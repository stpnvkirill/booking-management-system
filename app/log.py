import contextlib
import datetime
import logging
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, computed_field

from app.config import config

MSK_ZONE = ZoneInfo("Europe/Moscow")


def strip_filename(name: str):
    return "/app/" + name.split("/app/")[-1]


def get_error_source(error: Exception):
    """
    Get the line of code where the error occurred
    """
    try:
        exc_traceback = error.__traceback__

        if exc_traceback is None:
            return None

        tb = exc_traceback
        while tb is not None:
            frame = tb.tb_frame
            filename = frame.f_code.co_filename
            if (
                "site-packages" not in filename
                and "lib/python" not in filename
                and "<" not in filename
                and "logs.py" not in filename
            ):
                line_no = tb.tb_lineno
                try:
                    with open(filename, encoding="utf-8") as f:
                        lines = f.readlines()
                        if line_no - 1 < len(lines):
                            source_line = lines[line_no - 1].strip()
                            return {
                                "error": str(error),
                                "filename": f"{strip_filename(filename)}:{line_no}",
                                "source": source_line,
                            }
                except Exception:  # noqa: BLE001, S110
                    pass
                return {
                    "error": str(error),
                    "filename": f"{strip_filename(filename)}:{line_no}",
                    "source": "Couldn't read the line",
                }

            tb = tb.tb_next

        return None

    except Exception:  # noqa: BLE001
        return None


class Detail(BaseModel):
    detail: str | dict


class JsonLogSchema(BaseModel):
    datetime_msk: datetime.datetime
    level: str
    method: str
    path: str
    bot_id: int | None = None
    bot_username: str | None = None
    url: str | None = None
    ip: str | None = None
    status: int | None = None
    size: int | None = None
    duration: int | None = None
    raw_detail: str | None = Field(None, exclude=True)
    text_detail: str | None = Field(None, exclude=True)
    error: dict | None = None
    user: dict | None = None

    @computed_field
    @property
    def detail(self) -> str | dict | None:
        if self.raw_detail:
            try:
                d = Detail.model_validate_json(self.raw_detail)
                return d.detail
            except Exception:  # noqa: BLE001
                ...
        return self.text_detail


def log(  # noqa: PLR0913
    level: str,
    method: str,
    path: str,
    bot_id: int | None = None,
    bot_username: str | None = None,
    url: str | None = None,
    ip: str | None = None,
    status: int | None = None,
    size: int | None = None,
    duration: int | None = None,
    exception: Exception | None = None,
    raw_detail: str | None = None,
    text_detail: str | dict | None = None,
    user: dict | None = None,
):
    error = None
    if exception is not None:
        with contextlib.suppress(Exception):
            error = get_error_source(exception)

    model = JsonLogSchema.model_validate(
        {
            "datetime_msk": datetime.datetime.now(tz=MSK_ZONE),
            "level": level,
            "method": method,
            "path": path,
            "ip": ip,
            "url": url,
            "status": status,
            "size": size,
            "duration": duration,
            "error": error,
            "raw_detail": raw_detail,
            "text_detail": text_detail,
            "user": user,
            "bot_id": bot_id,
            "bot_username": bot_username,
        },
    )

    logging.info(model.model_dump_json(exclude_defaults=True, exclude_none=True))
    if config.server.EXCEPT_LOG and exception is not None:
        logging.exception(msg="Error", stack_info=True, stacklevel=1)
