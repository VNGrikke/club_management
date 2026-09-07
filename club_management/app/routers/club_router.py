from fastapi import APIRouter, Depends, Request, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database.db import get_db
from models.user import User
from schemas.club_schema import ClubCreate, ClubUpdate, ClubResponse
from schemas.ResponseApi import APIResponse
from services.user_services import get_current_user

from services.club_services import (create_club, get_my_clubs, get_club_detail, update_club, soft_delete_club,)

router_club = APIRouter(prefix="/clubs", tags=["Clubs"])


@router_club.post("", response_model=APIResponse[ClubResponse])
def create_club_endpoint(request: Request, data: ClubCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    club = create_club(data, current_user, db)
    return APIResponse(
        statusCode=status.HTTP_201_CREATED,
        message="Tạo câu lạc bộ thành công",
        data=club,
        path=request.url.path
    )

@router_club.get("", response_model=APIResponse[List[ClubResponse]])
def get_clubs_endpoint(
    request: Request,
    search: Optional[str] = Query(None, description="Tìm kiếm theo tên"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    clubs = get_my_clubs(current_user, db, search)
    return APIResponse(
        statusCode=status.HTTP_200_OK,
        message="Lấy danh sách câu lạc bộ thành công",
        data=clubs,
        path=request.url.path
    )

@router_club.get("/{club_id}", response_model=APIResponse[ClubResponse])
def get_club_detail_endpoint(request: Request, club_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    club = get_club_detail(club_id, current_user, db)
    return APIResponse(
        statusCode=status.HTTP_200_OK,
        message="Lấy thông tin chi tiết thành công",
        data=club,
        path=request.url.path
    )

@router_club.patch("/{club_id}", response_model=APIResponse[ClubResponse])
def update_club_endpoint(request: Request, club_id: int, data: ClubUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    club = update_club(club_id, data, current_user, db)
    return APIResponse(
        statusCode=status.HTTP_200_OK,
        message="Cập nhật câu lạc bộ thành công",
        data=club,
        path=request.url.path
    )

@router_club.delete("/{club_id}", response_model=APIResponse[None])
def delete_club_endpoint(request: Request, club_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    soft_delete_club(club_id, current_user, db)
    return APIResponse(
        statusCode=status.HTTP_200_OK,
        message="Xóa câu lạc bộ thành công",
        data=None,
        path=request.url.path
    )
