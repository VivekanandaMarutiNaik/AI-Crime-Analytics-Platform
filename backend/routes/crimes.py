from fastapi import APIRouter

router = APIRouter()

@router.get("/crimes")
def get_crimes():
    return {
        "message": "Crime API is working!",
        "data": []
    }