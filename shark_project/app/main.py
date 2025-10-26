# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import dicoms, auth
from app.models import Base
from app.db import engine

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORSMiddleware correctly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust "*" to specific frontend domains in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods like GET, POST, etc.
    allow_headers=["*"],  # Allows all headers
)

# Include the DICOM router
app.include_router(dicoms.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
