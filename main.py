import uvicorn

from app import get_application

app = get_application()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, log_level="error")  # noqa: S104
