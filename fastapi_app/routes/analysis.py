from fastapi import APIRouter

router = APIRouter()


@router.get("/test")
def test():
    return {"message": "Analysis route working!"}
