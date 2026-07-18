from fastapi import FastAPI
from backend.routes.crimes import router as crimes_router
from backend.routes.cctv import router as cctv_router
from backend.routes.hotspots import router as hotspots_router
from backend.routes.dashboard import router as dashboard_router
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.districts import router as districts_router
from backend.routes.case_routes import router as case_router
from backend.routes.analytics_routes import router as analytics_router
from backend.routes.ai import router as ai_router

app = FastAPI(
    title="AI Crime Analytics Platform",
    description="Backend APIs for Crime Analytics and CCTV Intelligence",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crimes_router)
app.include_router(cctv_router)
app.include_router(hotspots_router)
app.include_router(dashboard_router)
app.include_router(districts_router)
app.include_router(case_router)
app.include_router(analytics_router)
app.include_router(ai_router)

@app.get("/")
def root():
    return {
        "message": "AI Crime Analytics Platform API is running"
    }