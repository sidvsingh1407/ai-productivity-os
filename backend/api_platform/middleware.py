import time
from typing import Callable, Coroutine, Any
from fastapi import Request, Response
from fastapi.routing import APIRoute
from starlette.background import BackgroundTask

from database import async_session_maker
from models.api_platform import ApiUsageLog
from .service import ApiKeyService

async def log_api_usage(
    api_key_id: str,
    endpoint: str,
    request_method: str,
    response_status: int,
    latency_ms: float
):
    """Background task to save API usage and update last_used_at."""
    async with async_session_maker() as db:
        try:
            # Create usage log
            log = ApiUsageLog(
                api_key_id=api_key_id,
                endpoint=endpoint,
                request_method=request_method,
                response_status=response_status,
                latency_ms=latency_ms
            )
            db.add(log)

            # Update API Key last_used_at
            await ApiKeyService.update_last_used(db, api_key_id)

            await db.commit()
        except Exception as e:
            # We don't want a logging failure to crash anything, but we should probably log it to stdout
            print(f"Failed to log API usage: {e}")


class APIKeyRoute(APIRoute):
    """
    Custom APIRoute to measure latency and automatically inject a background task
    to log usage for authenticated API requests.
    """
    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        from fastapi import HTTPException
        from starlette.background import BackgroundTasks

        async def custom_route_handler(request: Request) -> Response:
            start_time = time.perf_counter()

            response = None
            exception_raised = None
            status_code = 500

            try:
                response = await original_route_handler(request)
                status_code = response.status_code
            except HTTPException as exc:
                exception_raised = exc
                status_code = exc.status_code
            except Exception as exc:
                exception_raised = exc
                status_code = 500

            end_time = time.perf_counter()
            latency_ms = (end_time - start_time) * 1000

            # Check if this request was authenticated with an API key
            if hasattr(request.state, "api_key"):
                api_key = request.state.api_key

                task = BackgroundTask(
                    log_api_usage,
                    api_key_id=api_key.id,
                    endpoint=request.url.path,
                    request_method=request.method,
                    response_status=status_code,
                    latency_ms=latency_ms
                )

                if response:
                    if response.background:
                        if isinstance(response.background, BackgroundTasks):
                            response.background.add_task(
                                log_api_usage,
                                api_key_id=api_key.id,
                                endpoint=request.url.path,
                                request_method=request.method,
                                response_status=status_code,
                                latency_ms=latency_ms
                            )
                        else:
                            tasks = BackgroundTasks()
                            tasks.add_task(response.background.func, *response.background.args, **response.background.kwargs)
                            tasks.add_task(
                                log_api_usage,
                                api_key_id=api_key.id,
                                endpoint=request.url.path,
                                request_method=request.method,
                                response_status=status_code,
                                latency_ms=latency_ms
                            )
                            response.background = tasks
                    else:
                        response.background = task
                else:
                    # If an exception was raised, we need to inject the background task
                    # This is tricky because an unhandled exception will skip standard response generation.
                    # As a simpler approach we'll log it directly via asyncio.create_task to ensure it happens.
                    import asyncio
                    asyncio.create_task(
                        log_api_usage(
                            api_key_id=api_key.id,
                            endpoint=request.url.path,
                            request_method=request.method,
                            response_status=status_code,
                            latency_ms=latency_ms
                        )
                    )

            if exception_raised:
                raise exception_raised

            return response

        return custom_route_handler
