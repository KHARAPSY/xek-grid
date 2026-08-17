from fastapi import APIRouter

from .health import health_router
from .v1 import v1_router

rag_router = APIRouter(prefix="/rag", tags=["RAG Service"])

rag_router.include_router(health_router)
rag_router.include_router(v1_router)

