# Libs
from fastapi import FastAPI  # FastAPI
from fastapi.middleware.cors import CORSMiddleware  # FastAPI CORS

# Application
from routers import auth, counter

# FastAPI
app: FastAPI = FastAPI(
    title="Since Porject - BackEnd",
    version="0.1.0",
    summary="BackEnd service of Since.",
    openapi_tags=[
        {"name": "Authentication", "description": "Authentication endpoints"},
        {"name": "Counter", "description": "Counter endpoints"},
    ],
    servers=[
        {
            "url": "https://since.amirhossein.info",
            "description": "Since Production Server",
        },
        {
            "url": "http://127.0.0.1:8000",
            "description": "Development",
        },
    ],
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[
        "https://since.amirhossein.info",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-API-KEY"],
)

# Routers
app.include_router(auth.router, prefix="/api")  # Authentication
app.include_router(counter.router, prefix="/api")  # Counter
