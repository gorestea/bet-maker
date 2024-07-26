from fastapi import FastAPI
from app.api import router
from app.db import init_db


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(router)

