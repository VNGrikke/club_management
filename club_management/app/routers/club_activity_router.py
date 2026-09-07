from fastapi import APIRouter, Depends, Request, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database.db import get_db
from models.user import User
from models.enums import ActivityStatus, ActivityPriority, Order, SortBy
from schemas.club_activity_schema import ClubActivityCreate, ClubActivityUpdate, ClubActivityResponse, DetailClubActivityResponse
from schemas.ResponseApi import APIResponse
from services.user_services import get_current_user

# Import các hàm từ service
from services.club_activity_services import (
    create_activity, get_club_activities, get_activity_detail, 
    update_activity, delete_activity
)

router_activities = APIRouter(tags=["Activities"])


@router_activities.post("/clubs/{club_id}/activities", response_model=APIResponse[ClubActivityResponse])
def create_club_activity_endpoint(
    request: Request, club_id: int, data: ClubActivityCreate, 
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    activity = create_activity(club_id, data, current_user, db)
    return APIResponse(
        statusCode=status.HTTP_201_CREATED,
        message="Tạo hoạt động câu lạc bộ thành công",
        data=activity,
        path=request.url.path
    )

@router_activities.get("/clubs/{club_id}/activities", response_model=APIResponse[List[ClubActivityResponse]])
def get_club_activities_endpoint(
    request: Request,
    club_id: int,
    search: Optional[str] = Query(None, description="Tìm kiếm theo tiêu đề (title)"),
    status_filter: Optional[ActivityStatus] = Query(None, alias="status", description="Lọc theo TODO/IN_PROGRESS/DONE"),
    priority: Optional[ActivityPriority] = Query(None, description="Lọc theo LOW/MEDIUM/HIGH"),
    assignee_id: Optional[int] = Query(None, description="Lọc theo người được giao"),
    sort_by: Optional[SortBy] = Query(SortBy.CREATE_AT, description="Sắp xếp theo 'created_at' hoặc 'due_date'"),
    order: Optional[Order] = Query(Order.ASC, description="Thứ tự 'asc' hoặc 'desc'"),
    page: int = Query(1, ge=1, description="Số trang (bắt đầu từ 1)"),
    size: int = Query(10, ge=1, le=100, description="Kích thước trang"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    activities = get_club_activities(
        club_id, current_user, db, search, status_filter, priority, 
        assignee_id, sort_by, order, page, size
    )
    return APIResponse(
        statusCode=status.HTTP_200_OK,
        message="Lấy danh sách hoạt động thành công",
        data=activities,
        path=request.url.path
    )



@router_activities.get("/activities/{activity_id}", response_model=APIResponse[DetailClubActivityResponse])
def get_activity_detail_endpoint(
    request: Request, activity_id: int, 
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    activity = get_activity_detail(activity_id, current_user, db)
    return APIResponse(
        statusCode=status.HTTP_200_OK,
        message="Lấy chi tiết hoạt động thành công",
        data=activity,
        path=request.url.path
    )

@router_activities.patch("/activities/{activity_id}", response_model=APIResponse[ClubActivityResponse])
def update_activity_endpoint(
    request: Request, activity_id: int, data: ClubActivityUpdate, 
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    activity = update_activity(activity_id, data, current_user, db)
    return APIResponse(
        statusCode=status.HTTP_200_OK,
        message="Cập nhật hoạt động thành công",
        data=activity,
        path=request.url.path
    )

@router_activities.delete("/activities/{activity_id}", response_model=APIResponse[None])
def delete_activity_endpoint(
    request: Request, activity_id: int, 
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    delete_activity(activity_id, current_user, db)
    return APIResponse(
        statusCode=status.HTTP_200_OK,
        message="Xóa hoạt động thành công",
        data=None,
        path=request.url.path
    )