from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    model: str = Field(
        "",
        description="The name of the AI model to use for generating responses."
    )
    question: str = Field(
       "What is the capital of Thailand?", 
        description="The question to be answered by the AI model."
    )


class Reasoning(BaseModel):
    role: str = Field(
        ...,
        description="The role associated with the reasoning process",
    )
    reason: str = Field(
        ...,
        description="Extracted thinking or step-by-step reasoning process",
    )

class CompletionDetail(BaseModel):
    answer: str = Field(
        ..., description="The final parsed answer stripped of thinking tags"
    )
    reasoning: Reasoning = Field(
        ..., description="Nested reasoning and role breakdown"
    )

class ChatResponse(BaseModel):
    model: str = Field(
        ..., description="The model name that generated the response"
    )
    input_tokens: int = Field(
        default=0, ge=0, description="Tokens used for the prompt input"
    )
    output_tokens: int = Field(
        default=0, ge=0, description="Tokens generated in the completion"
    )
    completions: CompletionDetail = Field(
        ..., description="Detailed completion results including answer and model info"
    )

