from app.core.llm import chat
from app.core.logger import logger


def code(plan: str) -> str:
    logger.info("开始编写代码...")
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个高级程序员。"
                "请根据下面的方案编写 Python 代码。"
                "只返回代码，不要额外解释。"
            ),
        },
        {"role": "user", "content": plan},
    ]
    return chat(messages)
