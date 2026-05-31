from app.core.llm import chat
from app.core.logger import logger


def review(code: str) -> str:
    logger.info("开始审查代码...")
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个资深代码审查员。"
                "检查下面的代码是否有问题。"
                "如果有问题，返回需要修改的地方；"
                "如果没问题，返回 'PASS'。"
            ),
        },
        {"role": "user", "content": code},
    ]
    return chat(messages)
