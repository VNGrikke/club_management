from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.club_activity import ClubActivity
from models.club_member import ClubMember
from models.user import User
from models.enums import MemberRole, ActivityStatus, ActivityPriority
from schemas.club_activity_schema import ClubActivityCreate, ClubActivityUpdate

# --- HELPER: Kiểm tra tư cách thành viên ---
def get_member_role(club_id: int, user_id: int, db: Session) -> MemberRole:
    """Lấy vai trò của user trong câu lạc bộ. Trả về 403 nếu không phải thành viên."""
    member = db.query(ClubMember).filter(
        ClubMember.club_id == club_id, 
        ClubMember.user_id == user_id
    ).first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Bạn không phải thành viên của câu lạc bộ này"
        )
    return member.role


# --- MAIN SERVICES ---
def create_activity(club_id: int, data: ClubActivityCreate, current_user: User, db: Session) -> ClubActivity:
    # Bắt buộc phải là thành viên mới được tạo hoạt động
    get_member_role(club_id, current_user.id, db)
    
    # Giao việc: Xác thực assignee phải nằm trong câu lạc bộ
    if data.assignee_id:
        assignee = db.query(ClubMember).filter(
            ClubMember.club_id == club_id, 
            ClubMember.user_id == data.assignee_id
        ).first()
        if not assignee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Người được giao việc (Assignee) phải là thành viên của câu lạc bộ"
            )
            
    new_activity = ClubActivity(
        club_id=club_id,
        title=data.title,
        description=data.description,
        assignee_id=data.assignee_id,
        status=data.status,
        priority=data.priority,
        due_date=data.due_date
    )
    
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity


def get_club_activities(
    club_id: int, current_user: User, db: Session,
    search: str = None, status_filter: ActivityStatus = None, 
    priority: ActivityPriority = None, assignee_id: int = None,
    sort_by: str = "created_at", order: str = "desc",
    page: int = 1, size: int = 10
) -> list[ClubActivity]:
    
    get_member_role(club_id, current_user.id, db)
    
    query = db.query(ClubActivity).filter(ClubActivity.club_id == club_id)
    
    # Lọc & Tìm kiếm
    if search:
        query = query.filter(ClubActivity.title.ilike(f"%{search}%"))
    if status_filter:
        query = query.filter(ClubActivity.status == status_filter)
    if priority:
        query = query.filter(ClubActivity.priority == priority)
    if assignee_id:
        query = query.filter(ClubActivity.assignee_id == assignee_id)
        
    # Sắp xếp
    if sort_by == "due_date":
        query = query.order_by(ClubActivity.due_date.desc() if order == "desc" else ClubActivity.due_date.asc())
    else:
        query = query.order_by(ClubActivity.created_at.desc() if order == "desc" else ClubActivity.created_at.asc())
        
    # Phân trang
    offset = (page - 1) * size
    return query.offset(offset).limit(size).all()


def get_activity_detail(activity_id: int, current_user: User, db: Session) -> ClubActivity:
    activity = db.query(ClubActivity).filter(ClubActivity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hoạt động không tồn tại")
        
    # Xác thực quyền xem
    get_member_role(activity.club_id, current_user.id, db)
    return activity


def update_activity(activity_id: int, data: ClubActivityUpdate, current_user: User, db: Session) -> ClubActivity:
    activity = db.query(ClubActivity).filter(ClubActivity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hoạt động không tồn tại")
        
    role = get_member_role(activity.club_id, current_user.id, db)
    
    # Permission Matrix: Chỉ OWNER hoặc ASSIGNEE mới có quyền sửa
    if role != MemberRole.OWNER and activity.assignee_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Chỉ Chủ câu lạc bộ (OWNER) hoặc Người được giao việc (Assignee) mới có quyền cập nhật"
        )
        
    # Chỉ OWNER mới được quyền thay đổi người phụ trách (assignee_id)
    if data.assignee_id is not None and data.assignee_id != activity.assignee_id:
        if role != MemberRole.OWNER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Chỉ Chủ câu lạc bộ mới có quyền giao việc cho người khác"
            )
        # Xác thực assignee mới
        assignee_member = db.query(ClubMember).filter(
            ClubMember.club_id == activity.club_id, 
            ClubMember.user_id == data.assignee_id
        ).first()
        if not assignee_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Người được giao việc phải là thành viên của câu lạc bộ"
            )

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(activity, key, value)
        
    db.commit()
    db.refresh(activity)
    return activity


def delete_activity(activity_id: int, current_user: User, db: Session):
    activity = db.query(ClubActivity).filter(ClubActivity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hoạt động không tồn tại")
        
    role = get_member_role(activity.club_id, current_user.id, db)
    
    # Permission Matrix: Chỉ OWNER mới có quyền xóa
    if role != MemberRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Chỉ Chủ câu lạc bộ (OWNER) mới có quyền xóa hoạt động"
        )
        
    db.delete(activity)
    db.commit()