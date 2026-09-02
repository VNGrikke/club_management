from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# 1. Định nghĩa các Custom Exceptions
class BaseAPIException(Exception):
    """Lớp base cho mọi custom exception trong hệ thống"""
    def __init__(self, message: str, status_code: int, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details

class BadRequestException(BaseAPIException):
    def __init__(self, message: str = "Dữ liệu không hợp lệ", details: dict = None):
        super().__init__(message=message, status_code=400, details=details)

class ForbiddenException(BaseAPIException):
    def __init__(self, message: str = "Bạn không có quyền thực hiện hành động này", details: dict = None):
        super().__init__(message=message, status_code=403, details=details)

class NotFoundException(BaseAPIException):
    def __init__(self, message: str = "Không tìm thấy tài nguyên", details: dict = None):
        super().__init__(message=message, status_code=404, details=details)


# 2. Hàm Format Response Lỗi Thống Nhất
def unified_error_response(status_code: int, message: str, details: any = None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "code": status_code,
            "message": message,
            "details": details
        }
    )

# 3. Đăng ký các Exception Handlers
def setup_exception_handlers(app):
    
    # Xử lý các Custom Exception(400, 403, 404)
    @app.exception_handler(BaseAPIException)
    def custom_api_exception_handler(request: Request, exc: BaseAPIException):
        return unified_error_response(
            status_code=exc.status_code,
            message=exc.message,
            details=exc.details
        )

    # Xử lý lỗi validation của Pydantic (422)
    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = [{"field": err["loc"][-1], "msg": err["msg"]} for err in exc.errors()]
        return unified_error_response(
            status_code=422,
            message="Dữ liệu đầu vào không đúng định dạng",
            details=errors
        )

    # Xử lý các HTTP Exception mặc định của FastAPI/Starlette
    @app.exception_handler(StarletteHTTPException)
    def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return unified_error_response(
            status_code=exc.status_code,
            message=exc.detail
        )

    # Xử lý lỗi 500 (Catch-all cho các lỗi code/logic chưa được bắt)
    @app.exception_handler(Exception)
    def general_exception_handler(request: Request, exc: Exception):
        print(f"Bugs: {exc}") 
        return unified_error_response(
            status_code=500,
            message="Lỗi máy chủ nội bộ. Vui lòng thử lại sau.",
            details=str(exc) 
        )