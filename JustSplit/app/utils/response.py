from fastapi import (
    status,
    Response
)
from pydantic import BaseModel, conint, constr
from typing import Any


class SuccessResponseSerializer(BaseModel):
    code: conint() = status.HTTP_200_OK
    status: constr() = "Success"
    message: constr()
    data: Any = None
    
class ErrorResponseSerializer(BaseModel):
    code: conint() = status.HTTP_500_INTERNAL_SERVER_ERROR
    status: constr() = "Error"
    message: constr()
    data: Any = None
    
def response_structure(serializer, status_code):
    return Response(
        content = serializer.json(),
        media_type="application/json",
        status_code=status_code
    )