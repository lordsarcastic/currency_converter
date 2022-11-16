import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router
from backend.settings import settings
from db.db import db


app = FastAPI(title=settings.APP_TITLE)

app.include_router(router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    origins=settings.ALLOWED_CLIENTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
