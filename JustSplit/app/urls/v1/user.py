from fastapi import APIRouter,Depends, Request,Form,File,UploadFile
from app.Auth.auth_bearer import JWTBearer
from app.Auth.auth_handler import verify_token,create_access_token
from fastapi_jwt_auth import AuthJWT
from app.api.user.controller import (
    UserController
)
from app.api.user.serializer import (
    EmailVerificationSerializer,
    CreateUserRequestSerializer
)

from typing import Optional
from pydantic import EmailStr

router = APIRouter(prefix="/api")
    

@router.get('/testing_api/')
async def testing_api(token: Request,authorize:AuthJWT=Depends()):
    return await UserController.test_api(token=token,authorize=authorize)

@router.post('/email_verification/')
async def email_verification(request:EmailVerificationSerializer,authorize:AuthJWT=Depends(),device_id:str = "",device_name:str = ""):
    return await UserController.email_verification(
        request=request,
        authorize=authorize,
        device_id=device_id,
        device_name=device_name
        )
    
# @router.post('/create_user/')
# async def create_user(request:CreateUserRequestSerializer,profile_image: UploadFile = File(),authorize:AuthJWT=Depends()):
#     return await UserController.create_user(
#         request=request,
#         profile_image=profile_image,
#         authorize=authorize
#     )
    
@router.post('/create_user/')
async def create_user(
        name: str = Form(),
        email: EmailStr = Form(),
        device_id: str = Form(),
        device_name: str = Form(),
        profile_image: UploadFile = File(),
        authorize:AuthJWT=Depends()
    ):
    return await UserController.create_user(
        name=name,
        email=email,
        device_id=device_id,
        device_name=device_name,
        profile_image=profile_image,
        authorize=authorize
    )

@router.post('/update_user/')
async def update_user(
        token: Request,
        authorize:AuthJWT=Depends(),
        name : Optional[str] = Form(None),
        user_name : Optional[str] = Form(None),
        email : Optional[EmailStr] = Form(None),
        phone_number : Optional[str] = Form(None),
        dob : Optional[str] = Form(None),
        profile_image: Optional[UploadFile] = File(None),
    ):
    return await UserController.update_user(
        token=token,
        authorize=authorize,
        name=name,
        user_name=user_name,
        email=email,
        phone_number=phone_number,
        dob=dob,
        profile_image=profile_image,
    )

# @router.post('/update_user/')
# async def update_user(
#         token: Request,
#         authorize:AuthJWT=Depends()
#     ):
#     return await UserController.update_user(
#         token=token,
#         authorize=authorize
#     )