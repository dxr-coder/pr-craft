from fastapi import FastAPI

from app.core.exceptions import AppException, app_exception_handler
from app.core.logger import logger
from app.core.middleware import setup_middleware
from app.routers import health, tasks

app = FastAPI(title="PR Craft")

setup_middleware(app)

app.add_exception_handler(AppException, app_exception_handler)

app.include_router(health.router)
app.include_router(tasks.router)


@app.get("/")
def root():
    logger.info("有人访问了首页")
    return {"message": "Hello ,PR Craft"}
