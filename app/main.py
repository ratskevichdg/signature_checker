from fastapi import FastAPI

from app.handlers import router


app = FastAPI()


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
