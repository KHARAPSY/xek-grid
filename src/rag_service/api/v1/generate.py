from fastapi import APIRouter

from src.rag_service.deps import openai_client as client
from src.common.schemas.rag import ChatRequest, ChatResponse
from src.common.helpers import RagHelper

router = APIRouter()

@router.post("/generate", response_model=ChatResponse, summary="Generate a response from the LLM")
def generate(request: ChatRequest):

    # 1. Guardrails - Validate the request
    # 2. Redis - Check if the response is cached in Redis
    result = RagHelper.prompt_template(request)

    # 3. OpenAI - Call completion API
    response = client.chat.completions.create(
        model=result[0],
        messages=result[1],
    )

    # 4. Guardrails - Validate the response
    # 5. MLFlow - Log trace, usages, tokens
    # 6. Redis - Cache the response in Redis

    # 7. Return the response to the user
    return RagHelper.parse_llm_response(response, request.question)

