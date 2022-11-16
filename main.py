import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from backend.routes import router
from backend.settings import settings
from db.db import db


app = FastAPI(title=settings.APP_TITLE)

app.include_router(router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_CLIENTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def home():
    print(settings.ALLOWED_CLIENTS)
    logging.info(settings.ALLOWED_CLIENTS)
    res = RedirectResponse(url="/redoc")
    return res


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


# if __name__ == "__main__":
#     """
#     Server configurations
#     """
#     uvicorn.run(
#         app="main:app",
#         host=settings.ALLOWED_HOST,
#         debug=settings.DEBUG,
#         port=settings.ALLOWED_PORT,
#         reload=True,
#         log_level=logging.INFO,
#         use_colors=True,
#     )