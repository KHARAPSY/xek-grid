from fastapi import APIRouter

from src.rag_service.deps import openai_client as client

health_router = APIRouter()

@health_router.get("/health", summary="Check the health of the RAG service")
def health():
    """
    Check the health of the RAG service by making a test call to the OpenAI API.
    Returns a JSON response indicating the status of the service.
    """
    try:
        # Make a test call to the OpenAI API to check if it's reachable
        client.models.list()
        return {"status": "healthy", "message": "RAG service is healthy and reachable."}
    except Exception as e:
        return {"status": "unhealthy", "message": f"RAG service is unhealthy: {str(e)}"}

