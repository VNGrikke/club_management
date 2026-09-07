from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from database.db import get_db
from models.user import User
from models.enums import UserRole
from core.security import verify_access_token, security_bearer

# --- DEPENDENCIES XÁC THỰC ---
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_bearer), db: Session = Depends(get_db)) -> User:
    token = credentials.credentials
    payload = verify_access_token(token)
    user_id = payload.get("id_user")
    
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token không chứa thông tin người dùng")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tài khoản người dùng")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tài khoản bị khóa")
        
    return user


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không đủ quyền thực hiện hành động này")
    return current_user


# --- LOGIC NGHIỆP VỤ ---
def fetch_all_users(db: Session, search: Optional[str] = None, is_active: Optional[bool] = None) -> list[User]:
    query = db.query(User)
    
    if search:
        search_fmt = f"%{search}%"
        query = query.filter(
            (User.full_name.ilike(search_fmt)) | (User.email.ilike(search_fmt))
        )
        
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
        
    return query.all()