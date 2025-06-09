from fastapi import FastAPI
from app.api.v1.routes import routes

app = FastAPI()

app.include_router(routes.router, prefix="/api/v1")
