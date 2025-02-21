from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core import config
app = FastAPI()

app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)
app.include_router(api_router, prefix="/api")

