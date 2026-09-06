from enum import IntEnum


# ==================== 定义数字错误码枚举 ====================
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

    # ====== 认证相关（新增） ======
    TOKEN_MISSING = 2006  # 未提供 token
    TOKEN_INVALID = 2007  # token 无效（签名错误、格式错误）
    TOKEN_EXPIRED = 2008  # token 已过期
    TOKEN_BLACKLISTED = 2009  # token 已登出（在黑名单）
    TOKEN_MISSING_JTI = 2010  # token 缺少 jti

    # 订单模块 3000-3999
    ORDER_NOT_FOUND = 3001
    ORDER_STATUS_ERROR = 3002
    INSUFFICIENT_BALANCE = 3003

    # 系统级错误 9000-9999
    DB_ERROR = 9001
    REDIS_ERROR = 9002
    THIRD_PARTY_ERROR = 9003
    SERVER_ERROR = 9999


# ==================== 定义错误码对应的提示信息 ====================
biz_code_messages = {
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
    # ====== 认证相关（新增） ======
    BizCode.TOKEN_MISSING: "未提供 token",
    BizCode.TOKEN_INVALID: "无效 token，请重新登录",
    BizCode.TOKEN_EXPIRED: "token 已过期，请重新登录",
    BizCode.TOKEN_BLACKLISTED: "token 已登出，请重新登录",
    BizCode.TOKEN_MISSING_JTI: "token 格式异常，请重新登录",
}
