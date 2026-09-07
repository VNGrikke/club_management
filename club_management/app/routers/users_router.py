from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database.db import get_db
from models.user import User
from schemas.user_schema import UserResponse
from schemas.ResponseApi import APIResponse
from services.user_services import get_current_user, get_current_admin, fetch_all_users

router_user = APIRouter(prefix="/users", tags=["User"])

@router_user.get("/me", response_model=APIResponse[UserResponse])
def get_my_profile(request: Request, current_user: User = Depends(get_current_user)):
    return APIResponse(
        statusCode=status.HTTP_200_OK,
        message="Lấy thông tin cá nhân thành công",
        data=current_user,
        path=request.url.path
    )


@router_user.get("", response_model=APIResponse[List[UserResponse]])
def get_all_users_endpoint(
    request: Request,
    search: Optional[str] = Query(None, description="Tìm theo tên/email"),
    is_active: Optional[bool] = Query(None, description="Lọc trạng thái"),
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    users = fetch_all_users(db=db, search=search, is_active=is_active)
    
    return APIResponse(
        statusCode=status.HTTP_200_OK,
        message="Lấy danh sách người dùng thành công",
        data=users,
        path=request.url.path
    )