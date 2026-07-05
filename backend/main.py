from fastapi import FastAPI
from sqlalchemy import text

from backend.config.database import Base, engine
from backend.models.crime_case import CrimeCase
from backend.routes.crimes import router as crime_router

app = FastAPI(
    title="Karnataka Crime Analytics API",
    version="1.0.0"
)

# Create all database tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(crime_router)

# Test database connection on startup
@app.on_event("startup")
def startup():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("✅ Database connection successful!")

# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to Karnataka Crime Analytics API"
    }