import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.api_entrypoint:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        log_level=settings.API_LOG_LVL,
    )
