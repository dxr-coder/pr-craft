import sys

from loguru import logger


def set_logger():
    logger.remove()
    logger.add(
        sys.stderr,
        format=(
            "<green>{time:YYYY-MM-D HH:mm:ss}</green>"
            " | <level>{level: <8}</level>"
            " | <cyan>{name}</cyan>:<cyan>{line}</cyan>"
            " - <level>{message}</level>"
        ),
        level="INFO",
        colorize=True,
    )


set_logger()
