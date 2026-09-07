from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user import User
from schemas.user_schema import UserCreate, UserLogin
from core.security import (
    hash_password, 
    verify_password, 
    create_access_token, 
    create_refresh_token, 
    verify_access_token
)

def register_user(data: UserCreate, db: Session) -> User:
    user_existed = db.query(User).filter(User.email == data.email).first()
    if user_existed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email đã tồn tại",
        )

    user = User(
        email=data.email, 
        password_hash=hash_password(data.password), 
        full_name=data.full_name
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(data: UserLogin, db: Session) -> dict:
    user = db.query(User).filter(User.email == data.email).first()
    
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác"
        )
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản không hoạt động"
        )

    token_payload = {
        "id_user": str(user.id),
        "user_name": user.full_name,
        "role": user.role.value
    }

    return {
        "access_token": create_access_token(data=token_payload),
        "refresh_token": create_refresh_token(data=token_payload),
        "token_type": "bearer"
    }


def refresh_access_token(refresh_token: str) -> dict:
    try:
        payload = verify_access_token(refresh_token)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Refresh token không hợp lệ hoặc đã hết hạn"
        )
        
    new_payload = {
        "id_user": payload.get("id_user"),
        "user_name": payload.get("user_name"),
        "role": payload.get("role")
    }
    
    return {
        "access_token": create_access_token(data=new_payload), 
        "token_type": "bearer"
    }