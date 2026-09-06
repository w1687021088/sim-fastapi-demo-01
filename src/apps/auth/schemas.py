from pydantic import BaseModel, Field, field_validator, ValidationInfo
import re
from typing import Annotated


class AuthRegisterBody(BaseModel):
    """注册请求体"""
    username: str

    password: str

    confirm_password: str

    phone: Annotated[str | None, Field(examples=["13800138000"], description="手机号码")] = None

    email: Annotated[str | None, Field(examples=["example@example.com"], description="邮箱地址")] = None

    @field_validator("confirm_password")
    def validate_confirm_password(cls, v: str, info: ValidationInfo) -> str:
        if v != info.data.get("password"):
            raise ValueError("两次输入的密码不一致")
        return v

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        if not (8 <= len(v) <= 32):
            raise ValueError("密码长度必须为 8~32 位")

        allowed = r"^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};:'\",.<>/?|\\~`]+$"
        if not re.match(allowed, v):
            raise ValueError("密码只能包含字母、数字和常见特殊符号（如 !@#$%^&* 等）")

        if not re.search(r"\d", v):
            raise ValueError("密码必须包含至少一个数字")

        if not re.search(r"[^A-Za-z0-9]", v):
            raise ValueError("密码必须包含至少一个特殊符号（如 !@#$%^&* 等）")

        return v

    @field_validator("phone")
    def validate_phone(cls, v: str | None) -> str | None:
        if v is None:
            return v

        cleaned = re.sub(r"[\s\-()]", "", v)

        if not cleaned.isdigit():
            raise ValueError("手机号只能包含数字")

        if len(cleaned) != 11:
            raise ValueError("手机号必须为 11 位")

        if not cleaned.startswith("1"):
            raise ValueError("手机号必须以 1 开头")

        return v

    @field_validator("email")
    def validate_email(cls, v: str | None) -> str | None:
        if v is None:
            return v

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("邮箱格式不正确")

        if len(v) > 255:
            raise ValueError("邮箱地址不能超过 255 个字符")

        return v


class AuthRegisterResponse(BaseModel):
    """注册响应"""
    token: str
