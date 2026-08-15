from openai import OpenAI

from src.common.config import settings

openai_client = OpenAI(base_url=settings.openai_base_url, api_key=settings.openai_api_key)
