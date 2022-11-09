import logging

import uvicorn
from fastapi import FastAPI

from backend.routes import router
from backend.settings import settings
from db.db import db


app = FastAPI(title=settings.APP_TITLE)

app.include_router(router, prefix="/api/v1")


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
