from openai import OpenAI
from app.core.config import settings

client = OpenAI(
    api_key=settings.api_key,
    base_url=settings.base_url,
)


def chat(messages: list) -> str:
    response = client.chat.completions.create(
        model="deepseek-v4-flash", messages=messages
    )
    return response.choices[0].message.content
