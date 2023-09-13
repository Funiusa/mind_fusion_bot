from app.api.api_v1.endpoints import users, messages, characters
from fastapi.routing import APIRouter

api_router = APIRouter()

api_router.include_router(router=users.router, tags=["Users"], prefix="/users")
api_router.include_router(router=messages.router, tags=["Messages"], prefix="/messages")
api_router.include_router(
    router=characters.router, tags=["Characters"], prefix="/characters"
)
