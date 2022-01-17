from memory_profiler import profile
import uvicorn
from fastapi import FastAPI
from loguru import logger

from app.handlers import router


# Set up logger
logger.add(
    "logs/api_logs.log",
    format="{time} :: {level} :: {message}",
    level="ERROR",
    rotation="1 MB",
    compression="zip"
)

app = FastAPI()


@profile
def get_application() -> FastAPI:
    """
    Run API.

    Returns:
        FastAPI: API.
    """
    application = FastAPI()
    application.include_router(router)
    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
