from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.club import Club
from models.club_member import ClubMember
from models.user import User
from models.enums import MemberRole
from .activity_log_services import log_activity
from services.club_services import get_club_detail

def add_member_to_club(club_id: int, target_user_id: int, user: User, db: Session) -> ClubMember:
    # Validate Club
    club = db.query(Club).filter(Club.id == club_id, Club.is_deleted == False).first()
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Câu lạc bộ không tồn tại")
    if club.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ OWNER mới được thêm thành viên")

    # Validate Target User
    target_user = db.query(User).filter(User.id == target_user_id).first()
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng cần thêm không tồn tại")

    # Validate Duplication
    existing_member = db.query(ClubMember).filter(ClubMember.club_id == club_id, ClubMember.user_id == target_user_id).first()
    if existing_member:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Người dùng đã là thành viên của câu lạc bộ")

    new_member = ClubMember(club_id=club_id, user_id=target_user_id, role=MemberRole.MEMBER)
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    
    log_activity(db, "ADD_MEMBER", user.id, club_id, f"Them thanh vien cau lac bo user_id: {target_user_id}")

    return new_member


def remove_member_from_club(club_id: int, target_user_id: int, user: User, db: Session):
    club = db.query(Club).filter(Club.id == club_id, Club.is_deleted == False).first()
    
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Câu lạc bộ không tồn tại")
    if club.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ OWNER mới được xóa thành viên")
    if club.owner_id == target_user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không thể xóa OWNER khỏi câu lạc bộ")

    member = db.query(ClubMember).filter(ClubMember.club_id == club_id, ClubMember.user_id == target_user_id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thành viên không tồn tại trong câu lạc bộ")

    db.delete(member)
    db.commit()
    log_activity(db, "REMOVE_MEMBER", user.id, club_id, f"Xoa thanh vien cau lac bo user_id: {target_user_id}")


def get_club_members(club_id: int, user: User, db: Session) -> list[ClubMember]:
    # Chỉ thành viên mới xem được danh sách
    get_club_detail(club_id, user, db) 
    return db.query(ClubMember).filter(ClubMember.club_id == club_id).all()