import logging
from kombu.exceptions import OperationalError

logger = logging.getLogger(__name__)

def safe_task_dispatch(task, *args, **kwargs):
    """
    Safely dispatches a Celery task.
    If the Celery broker (e.g., Redis) is unavailable, it falls back to
    synchronous execution. If synchronous execution fails, it catches the
    exception to avoid blocking the main request flow.
    """
    try:
        # Try to dispatch asynchronously via Celery
        return task.delay(*args, **kwargs)
    except OperationalError as e:
        task_name = getattr(task, 'name', str(task))
        logger.warning(
            f"Celery broker unavailable, falling back to synchronous execution for {task_name}. Error: {e}"
        )
    except Exception as e:
        task_name = getattr(task, 'name', str(task))
        logger.warning(
            f"Unexpected error when dispatching {task_name} to Celery, falling back to synchronous execution. Error: {e}"
        )

    # Fallback to synchronous execution
    try:
        return task(*args, **kwargs)
    except Exception as e:
        task_name = getattr(task, 'name', str(task))
        logger.error(
            f"Synchronous execution failed for {task_name}. Error: {e}"
        )
        # Return None or a generic failure dict if needed.
        # But we must NOT raise the exception to prevent crashing the main flow.
        return None
