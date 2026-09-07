from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.club import Club
from models.club_member import ClubMember
from models.user import User
from models.enums import MemberRole
from schemas.club_schema import ClubCreate, ClubUpdate
from .activity_log_services import log_activity

def create_club(data: ClubCreate, user: User, db: Session) -> Club:
    new_club = Club(name=data.name, description=data.description, owner_id=user.id)
    db.add(new_club)
    db.commit()
    db.refresh(new_club)

    new_member = ClubMember(club_id=new_club.id, user_id=user.id, role=MemberRole.OWNER)
    db.add(new_member)
    db.commit()

    log_activity(db, "CREATE_CLUB", user.id, new_club.id, f"Tao cau lac bo moi owner_id: {user.id}")
    return new_club


def get_my_clubs(user: User, db: Session, search: str = None) -> list[Club]:
    query = db.query(Club).join(ClubMember).filter(
        ClubMember.user_id == user.id,
        Club.is_deleted == False
    )
    if search:
        query = query.filter(Club.name.ilike(f"%{search}%"))

    return query.all()


def get_club_detail(club_id: int, user: User, db: Session) -> Club:
    club = db.query(Club).filter(Club.id == club_id, Club.is_deleted == False).first()
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Câu lạc bộ không tồn tại")
    
    is_member = db.query(ClubMember).filter(ClubMember.club_id == club_id, ClubMember.user_id == user.id).first()
    if not is_member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không phải thành viên của câu lạc bộ này")
    
    return club


def update_club(club_id: int, data: ClubUpdate, user: User, db: Session) -> Club:
    club = db.query(Club).filter(Club.id == club_id, Club.is_deleted == False).first()
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Câu lạc bộ không tồn tại")
    
    if club.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ OWNER mới có quyền cập nhật")

    if data.name: club.name = data.name
    if data.description: club.description = data.description
    
    db.commit()
    db.refresh(club)
    log_activity(db, "UPDATE_CLUB", user.id, club_id, f"Cap nhat cau lac bo cua user_id: {user.id}")
    return club


def soft_delete_club(club_id: int, user: User, db: Session):
    club = db.query(Club).filter(Club.id == club_id, Club.is_deleted == False).first()
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Câu lạc bộ không tồn tại")
        
    if club.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ OWNER mới có quyền xóa")

    club.is_deleted = True
    db.commit()
    log_activity(db, "DELETE_CLUB", user.id, club_id, f"Xoa cau lac bo : {club.name}")


