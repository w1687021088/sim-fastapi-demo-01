import datetime
from fastapi.responses import JSONResponse
from typing import Any, Optional, Annotated, Generic, TypeVar
from fastapi import status
from pydantic import Field, BaseModel

from src.config import BizCode


class AppResponse(JSONResponse):
    """ App Response """
    def __init__(self, data: Optional[dict[str, Any]] = None, status_code: int = status.HTTP_200_OK,
                 message: Optional[str] = 'Success',
                 **kwargs: Any):
        self.data = {
            'code': BizCode.SUCCESS,
            'data': data,
            'message': message,
             "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        self.data.update(kwargs)
        super().__init__(content=self.data, status_code=status_code)


T = TypeVar("T")

class CommonResponseModel(BaseModel, Generic[T]):
    """ Common Response Model """
    code: Annotated[BizCode, Field(..., description="业务代码")]
    data: T
    message: str
    timestamp: str