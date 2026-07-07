from fastapi import FastAPI
from backend.routes.crimes import router as crimes_router

app = FastAPI(
    title="AI Crime Analytics Platform",
    description="Backend APIs for Crime Analytics and CCTV Intelligence",
    version="1.0.0"
)

app.include_router(crimes_router)


@app.get("/")
def root():
    return {
        "message": "AI Crime Analytics Platform API is running"
    }