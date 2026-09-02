from fastapi import APIRouter

router_user = APIRouter(prefix="/users", tags=["User"])


@router_user.get("/me")
def get_current_user():
    return