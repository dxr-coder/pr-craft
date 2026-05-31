from fastapi import FastAPI

from app.core.logger import logger
from app.routers import health

app = FastAPI(title="PR Craft")

app.include_router(health.router)


@app.get("/")
def root():
    logger.info("有人访问了首页")
    return {"message": "Hello ,PR Craft"}
