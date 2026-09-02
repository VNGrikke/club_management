from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from database.db import get_db
from club_management.app.schemas.user_schema import UserCreate, UserLogin
from services.auth_services import register, login

router_auth = APIRouter(prefix="/auth", tags=["Auth"])

@router_auth.post("/register")
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    user = register(data, db)
    return {"message" : "Dang ki tahnh cong", "user.id" : user.id}


@router_auth.post("/login")
def login_user(data: UserLogin, response: Response ,db: Session = Depends(get_db) ):
    token = login(data, db)
    
    return {
        "message": "dang nhap thahn cong",
        "access_token" : token}