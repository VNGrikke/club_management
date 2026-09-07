from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database.db import get_db
from schemas.user_schema import UserCreate, UserLogin, UserResponse
from schemas.ResponseApi import APIResponse
from services.auth_services import register_user, authenticate_user, refresh_access_token

router_auth = APIRouter(prefix="/auth", tags=["Auth"])

login_attempts = {}

def check_rate_limit(request: Request):
    client_ip = request.client.host
    now = datetime.now()
    attempts = login_attempts.get(client_ip, [])
    attempts = [t for t in attempts if now - t < timedelta(minutes=1)]
    
    if len(attempts) >= 5: 
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Quá nhiều yêu cầu đăng nhập. Vui lòng thử lại sau.")
    
    attempts.append(now)
    login_attempts[client_ip] = attempts


@router_auth.post("/register", response_model=APIResponse[UserResponse])
def register_endpoint(request: Request, data: UserCreate, db: Session = Depends(get_db)):
    user = register_user(data, db)
    return APIResponse(
        statusCode=status.HTTP_201_CREATED,
        message="Đăng ký tài khoản thành công",
        data=user,
        path=request.url.path
    )


@router_auth.post("/login", dependencies=[Depends(check_rate_limit)], response_model=APIResponse[dict])
def login_endpoint(request: Request, data: UserLogin, db: Session = Depends(get_db)):
    tokens = authenticate_user(data, db)
    return APIResponse(
        statusCode=status.HTTP_200_OK,
        message="Đăng nhập thành công",
        data=tokens,
        path=request.url.path
    )


@router_auth.post("/refresh", response_model=APIResponse[dict])
def refresh_endpoint(request: Request, refresh_token: str):
    new_token = refresh_access_token(refresh_token)
    return APIResponse(
        statusCode=status.HTTP_200_OK,
        message="Làm mới token thành công",
        data=new_token,
        path=request.url.path
    )