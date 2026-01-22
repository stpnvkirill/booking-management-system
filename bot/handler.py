import functools

from app.log import log


def handler(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        user = None
        try:
            user = kwargs.get("user")
        except Exception as e:  # noqa: BLE001
            log(
                level="ERROR",
                method="TG",
                path=func.__name__,
                text_detail=f"handler {func.__name__} called",
                user=f"{user}|<id:{user.id}>" if user else None,
                exception=e,
            )
        try:
            return await func(*args, **kwargs)
        except Exception as err:  # noqa: BLE001
            log(
                level="ERROR",
                method="TG",
                path=func.__name__,
                text_detail=f"handler {func.__name__} error",
                user=user.to_dict() if user else None,
                exception=err,
            )

    return wrapper
