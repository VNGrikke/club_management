from fastapi import APIRouter, Depends, Request, Query, status
from sqlalchemy.orm import Session
from typing import List

from database.db import get_db
from models.user import User
from schemas.club_member_schema import ClubMemberResponse
from schemas.ResponseApi import APIResponse
from services.user_services import get_current_user
from services.club_member_services import add_member_to_club, get_club_members, remove_member_from_club

router_club_member = APIRouter(prefix="/club_members", tags=["Club Members"])


@router_club_member.post("/{club_id}/members", response_model=APIResponse[ClubMemberResponse])
def add_member_endpoint(request: Request, club_id: int, user_id: int = Query(..., description="ID user cần thêm"), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    member = add_member_to_club(club_id, user_id, current_user, db)
    return APIResponse(
        statusCode=status.HTTP_201_CREATED,
        message="Thêm thành viên thành công",
        data=member,
        path=request.url.path
    )

@router_club_member.get("/{club_id}/members", response_model=APIResponse[List[ClubMemberResponse]])
def get_members_endpoint(request: Request, club_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    members = get_club_members(club_id, current_user, db)
    return APIResponse(
        statusCode=status.HTTP_200_OK,
        message="Lấy danh sách thành viên thành công",
        data=members,
        path=request.url.path
    )

@router_club_member.delete("/{club_id}/members/{user_id}", response_model=APIResponse[None])
def remove_member_endpoint(request: Request, club_id: int, user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    remove_member_from_club(club_id, user_id, current_user, db)
    return APIResponse(
        statusCode=status.HTTP_200_OK,
        message="Xóa thành viên thành công",
        data=None,
        path=request.url.path
    )