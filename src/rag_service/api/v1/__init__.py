from fastapi import APIRouter

from .generate import router as route_01

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(route_01)

