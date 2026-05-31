from fastapi import APIRouter

from app.core.logger import logger

router = APIRouter()


@router.get("/health")
def health_check():
    logger.info("健康检查被调用")
    return {"status": "ok"}
