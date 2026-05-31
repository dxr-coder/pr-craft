from app.core.llm import chat
from app.core.logger import logger


def plan(issue: str) -> str:
    logger.info("开始制定计划...")
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个资深架构师。请分析下面的需求，制定一个简要的实现方案。"
            ),
        },
        {"role": "user", "content": issue},
    ]
    return chat(messages)
