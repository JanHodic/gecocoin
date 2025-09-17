from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import engine, Base
from .settings import CORS_ORIGINS
from .routers import coins


Base.metadata.create_all(bind=engine)


app = FastAPI(title="Crypto CRUD API", version="1.0.0")


app.add_middleware(
CORSMiddleware,
allow_origins=CORS_ORIGINS,
allow_credentials=True,
allow_methods=["*"]
,allow_headers=["*"]
)


app.include_router(coins.router)


@app.get("/health")
async def health():
    return {"status": "ok"}