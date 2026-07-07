from fastapi import FastAPI
from backend.routes.crimes import router as crimes_router
from backend.routes.cctv import router as cctv_router
from backend.routes.hotspots import router as hotspots_router
from backend.routes.dashboard import router as dashboard_router

app = FastAPI(
    title="AI Crime Analytics Platform",
    description="Backend APIs for Crime Analytics and CCTV Intelligence",
    version="1.0.0"
)

app.include_router(crimes_router)
app.include_router(cctv_router)
app.include_router(hotspots_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {
        "message": "AI Crime Analytics Platform API is running"
    }