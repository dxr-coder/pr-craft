from fastapi import FastAPI
from app.routers import health

app = FastAPI(title="PR Craft")

app.include_router(health.router)


@app.get("/")
def root():
    return {"message": "Hello ,PR Craft"}
