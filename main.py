from fastapi import FastAPI
from app.controllers.webhook_controller import router

app = FastAPI()

app.include_router(router)
