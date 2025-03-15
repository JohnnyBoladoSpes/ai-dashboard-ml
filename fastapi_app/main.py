from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_app.routes import router

from fastapi_app.views.v1 import analysis as analysis_v1

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
