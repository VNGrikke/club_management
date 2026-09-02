from models.user import User
from club_management.app.schemas.user_schema import UserCreate, UserLogin
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from core.security import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

def register(data: UserCreate, db: Session):    
    user_existed = db.query(User).filter(User.email == data.email).first()

    if user_existed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email da ton tai")

    user = User(email=data.email, password_hash=hash_password(data.password), full_name=data.full_name)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login(data: UserLogin, db: Session):
    user_existed = db.query(User).filter(User.email == data.email).first()
    
    if not user_existed or not verify_password(data.password, user_existed.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoac mat khau khong dung!"
        )

    token_payload = {
        "id_user": str(user_existed.id),
        "user_name": user_existed.full_name,
        "role": user_existed.role
    }

    access_token = create_access_token(data=token_payload, exprice_delta = ACCESS_TOKEN_EXPIRE_MINUTES)

    
    
    return {access_token}