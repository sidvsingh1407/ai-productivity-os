import logging

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
    except Exception as e:
        task_name = getattr(task, 'name', str(task))
        logger.warning(
            f"Celery broker unavailable or error dispatching {task_name}, falling back to synchronous execution. Error: {e}"
        )

    # Fallback to synchronous execution
    try:
        try:
            return task(*args, **kwargs)
        except Exception as inner_e:
            task_name = getattr(task, 'name', str(task))
            logger.error(f"Synchronous execution failed for {task_name}. Error: {inner_e}")
            return None
    except Exception as e:
        task_name = getattr(task, 'name', str(task))
        logger.error(
            f"Failed to submit synchronous execution for {task_name}. Error: {e}"
        )
        return None
