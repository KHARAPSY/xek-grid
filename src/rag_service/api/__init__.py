from fastapi import APIRouter

from .v1 import v1_router

rag_router = APIRouter(prefix="/rag", tags=["RAG Service"])

rag_router.include_router(v1_router)

