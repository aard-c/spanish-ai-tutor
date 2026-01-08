from fastapi import FastAPI
from app.routes import chat
from .database import engine, Base

app = FastAPI()

app.include_router(chat.router, prefix="/chat")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)