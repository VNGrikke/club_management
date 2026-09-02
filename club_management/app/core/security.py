import bcrypt
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
import jwt

from core.config import settings

# Lấy trực tiếp các giá trị từ settings
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


# 1. XỬ LÝ MẬT KHẨU
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_bytes.decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


# 2. XỬ LÝ TOKEN (JWT)
# Hàm 1: TẠO TOKEN (Dùng khi Đăng nhập)
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    
    # Tính toán thời gian hết hạn (expiration time)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Tạo token (Encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Hàm 2: KIỂM TRA TOKEN 
def verify_access_token(token: str) -> dict:
    try:
        # Giải mã token (Decode)
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token đã hết hạn")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token không hợp lệ")