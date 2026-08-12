import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from api import api_router
from core.config import settings
from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    db_helper.dispose()
app = FastAPI()
app.include_router(api_router)
if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.run.host,
        port=settings.run.port
    )