from enum import IntEnum
from typing import Optional, Any
from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import datetime


# ==================== 0. 定义数字错误码枚举 ====================
class BizCode(IntEnum):
    """业务错误码（纯数字）"""
    SUCCESS = 0

    # 通用错误 1000-1999
    UNKNOWN_ERROR = 1000
    VALIDATION_ERROR = 1001
    NOT_FOUND = 1002
    BAD_REQUEST = 1003
    UNAUTHORIZED = 1004
    FORBIDDEN = 1005

    # 用户模块 2000-2999
    USER_NOT_FOUND = 2001
    USER_ALREADY_EXISTS = 2002
    USER_PASSWORD_ERROR = 2003
    USER_NOT_LOGIN = 2004
    USER_PERMISSION_DENIED = 2005

    # 订单模块 3000-3999
    ORDER_NOT_FOUND = 3001
    ORDER_STATUS_ERROR = 3002
    INSUFFICIENT_BALANCE = 3003

    # 系统级错误 9000-9999
    DB_ERROR = 9001
    REDIS_ERROR = 9002
    THIRD_PARTY_ERROR = 9003
    SERVER_ERROR = 9999


# ==================== 1. 通用业务异常 ====================
class AppException(Exception):
    """
    通用业务异常
    使用示例：
        raise AppException(BizCode.USER_NOT_FOUND, "用户不存在")
        raise AppException(BizCode.VALIDATION_ERROR, "参数校验失败", data={"field": "email"})
    """

    def __init__(
            self,
            code: BizCode = BizCode.UNKNOWN_ERROR,
            message: Optional[str] = None,
            data: Optional[Any] = None,
            http_status_code: int = status.HTTP_200_OK,  # 默认固定为 200
    ):
        # 如果没传 message，自动从错误码枚举中获取默认消息
        if message is None:
            message = self._get_default_message(code)
        self.code = code
        self.message = message
        self.data = data
        self.http_status_code = http_status_code
        super().__init__(self.message)

    @staticmethod
    def _get_default_message(code: BizCode) -> str:
        """为常见错误码提供默认文案"""
        default_messages = {
            BizCode.SUCCESS: "操作成功",
            BizCode.VALIDATION_ERROR: "请求参数校验失败",
            BizCode.NOT_FOUND: "请求的资源不存在",
            BizCode.USER_NOT_FOUND: "用户不存在",
            BizCode.USER_ALREADY_EXISTS: "用户已存在",
            BizCode.USER_PASSWORD_ERROR: "密码错误",
            BizCode.USER_NOT_LOGIN: "请先登录",
            BizCode.USER_PERMISSION_DENIED: "权限不足",
            BizCode.ORDER_NOT_FOUND: "订单不存在",
            BizCode.INSUFFICIENT_BALANCE: "余额不足",
            BizCode.SERVER_ERROR: "服务器内部错误，请稍后重试",
        }
        return default_messages.get(code, "未知错误")


# ==================== 2. 快捷函数（可选，让代码更简洁） ====================
def raise_biz_error(code: BizCode, message: Optional[str] = None, data: Optional[Any] = None):
    """快捷抛出业务异常"""
    raise AppException(code=code, message=message, data=data)


def handle_error(app: FastAPI) -> JSONResponse:
    # ==================== 3. 注册全局异常处理器 ====================

    # 3.1 处理所有自定义的业务异常
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.http_status_code,
            content={
                "success": False,
                "code": exc.code,
                "message": exc.message,
                "data": exc.data,
                "path": request.url.path
            }
        )

    # 3.2 处理 FastAPI 内置的 HTTP 异常
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        message = exc.detail or "请求处理失败"

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "code": exc.status_code,
                "message": message,
                "data": None,
                "path": request.url.path,
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
        )

    # 3.3 处理 Pydantic 参数校验失败异常 (RequestValidationError)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = [{"field": ".".join(str(l) for l in e["loc"]), "msg": e["msg"]} for e in exc.errors()]
        return JSONResponse(
            status_code=200,
            content={
                "success": False,
                "code": BizCode.VALIDATION_ERROR,
                "message": "请求参数校验失败",
                "data": errors,
                "path": request.url.path,
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
        )

    # 3.4 兜底处理所有未被捕获的系统异常
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, _: Exception):
        # ⚠️ 生产环境务必记录完整的堆栈日志，方便排查 Bug
        # logger.error(f"Unhandled system exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  # 改为 500
            content={
                "success": False,
                "code": BizCode.SERVER_ERROR,  # 9999
                "message": "服务器内部错误，请稍后重试",
                "data": None,
                "path": request.url.path,
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
        )
