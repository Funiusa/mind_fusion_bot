import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.services import init_db
from app.api.api_v1.api_routes import api_router

app = FastAPI(
    title=settings.PROJECT_NAME.title(),
    description=settings.PROJECT_DSC,
    debug=settings.API_DBG,
    version=settings.API_VS,
    openapi_url=settings.OPEN_API_URL,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def on_startup():
    try:
        logger.info("Initializing service")
        init_db()
        logger.info("Service finished initialize")
    except Exception as e:
        logger.error(e)
        raise e


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
app.mount("/characters/static", StaticFiles(directory="static"), name="static")
