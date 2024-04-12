from fastapi import status,Request

from app.api.user.schema import UserSchema,UserProfileSchema
from app.utils.send_mail import send_email
from app.utils.jwt import auth_check
from app.config.config import S3Config

from app.api.user.serializer import (
    UserResponseSerializer,
    EmailVerificationResponseSerializer,
    CreateUserResponseSerilizer
)

from app.utils.response import (
    ErrorResponseSerializer,
    SuccessResponseSerializer,
    response_structure
    )

import random

from datetime import timedelta


class UserController:
    
    @classmethod
    async def test_api(cls,token:Request,authorize):
        
        
        await auth_check(Authorize=authorize,token=token)
        user_id = authorize.get_jwt_subject()

        user = await UserSchema.test_data(int(user_id))
        
        data = UserResponseSerializer(
            id=user.id,
            name=user.name,
            user_name=user.user_name,
            profile_image= user.profile_image,
            email=user.email,
            phone_number=user.phone_number,
            dob=user.dob,
            friends=user.friends,
            Group=user.Group,
            current_currency=user.current_currency,
            all_currency_used=user.all_currency_used,
            device_ids=user.device_ids,
            created_at=str(user.created_at),
        )
        serializer = SuccessResponseSerializer(
            message='data get',
            code=status.HTTP_200_OK,
            data = data
        )
        return response_structure(
            serializer=serializer,
            status_code=status.HTTP_200_OK
        )
        
    @classmethod
    async def email_verification(cls,request,authorize,device_id,device_name):
        try:
            otp_num = random.randint(10000, 99999)
            recipient = request.recipient
            subject = request.subject
            
            user = await UserSchema.get_user(email=recipient)
            
            if user:
                if device_id:
                    if user.device_ids != None:
                        exist_device = []
                        for device in user.device_ids:
                            exist_device.append(device)
                        if not device_id in exist_device:
                            exist_device.append(device_id)
                            device_update = await UserSchema.update_devices(
                                user_id=user.id,
                                value_dict={
                                    'device_ids' : exist_device
                                }
                            )
                    else:
                        device_update = await UserSchema.update_devices(
                                user_id=user.id,
                                value_dict={
                                    'device_ids' : [device_id]
                                }
                            )
                access_token = authorize.create_access_token(subject=str(user.id),expires_time=timedelta(days=5))
                refresh_token = authorize.create_refresh_token(subject=str(user.id),expires_time=False)
                
                device_details = await UserSchema.add_device_login_details(
                    user=user,
                    device_id=device_id,
                    device_name=device_name
                    )
                
                user_data = {
                    'id':user.id,
                    'name':user.name,
                    'user_name':user.user_name,
                    'profile_image':user.profile_image,
                    'phone_number':user.phone_number,
                    'email':user.email,
                    'dob':user.dob,
                    'current_currency':user.current_currency,
                    'device_id':user.device_ids,
                    'created_at':str(user.created_at),
                }
                
                data = EmailVerificationResponseSerializer(
                    user=user_data,
                    token=access_token,
                    refresh_token=refresh_token,
                    otp=otp_num
                )
                serializer = SuccessResponseSerializer(
                    code=status.HTTP_200_OK,
                    message='User Already Exists',
                    data=data
                )
                
                response = response_structure(
                    serializer=serializer,
                    status_code=status.HTTP_200_OK
                )
            else:
                user_data = {
                    "id": None,
                    "name": None,
                    "user_name": None,
                    "profile_image": None,
                    "phone_number": None,
                    "email": None,
                    "dob": None,
                    "current_currency": None,
                    "device_id": None,
                    "created_at": None,
                }
                data = EmailVerificationResponseSerializer(
                    user=user_data,
                    token=None,
                    refresh_token=None,
                    otp=otp_num
                )
                serializer = SuccessResponseSerializer(
                    code=status.HTTP_404_NOT_FOUND,
                    message='User Not Found',
                    data=data
                )
                
                response = response_structure(
                    serializer=serializer,
                    status_code=status.HTTP_404_NOT_FOUND
                )
                
            sent_email = await send_email(recipient,subject,otp_num)
                
        except Exception as e:
            serializer = ErrorResponseSerializer(
                    code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message=f'Error : {e}',
                    data=None
                )
                
            response = response_structure(
                serializer=serializer,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response
    
    # async def create_user(cls,request,profile_image,authorize):
    @classmethod
    async def create_user(cls,name,email,device_id,device_name,profile_image,authorize):
        try:
        #     user = await UserSchema.get_user(email=request.email)
            
            user = await UserSchema.get_user(email=email)
            if user:
                serializer = ErrorResponseSerializer(
                    code=status.HTTP_302_FOUND,
                    message='User Already Exist',
                    data=None
                )
                
                response = response_structure(
                    serializer=serializer,
                    status_code=status.HTTP_302_FOUND
                )
            else:
                profile_image = S3Config.upload_image(profile_image)
        #         user = await UserSchema.create_user(
        #             name=request.name,
        #             profile_image=profile_image,
        #             email=request.email,
        #             device_id=request.device_id,
        #             device_name=request.device_name
        #         )
                user = await UserSchema.create_user(
                    name=name,
                    profile_image=profile_image,
                    email=email,
                    device_id=device_id
                )
                print(user.id)
                
                access_token = authorize.create_access_token(subject=str(user.id),expires_time=timedelta(days=5))
                refresh_token = authorize.create_refresh_token(subject=str(user.id),expires_time=False)

                device_details = await UserSchema.add_device_login_details(
                    user=user,
                    device_id=device_id,
                    device_name=device_name
                )
                
                user_data = {
                    'id':user.id,
                    'name':user.name,
                    'user_name':user.user_name,
                    'profile_image':user.profile_image,
                    'phone_number':user.phone_number,
                    'email':user.email,
                    'dob':user.dob,
                    'current_currency':user.current_currency,
                    'device_id':user.device_ids,
                    'created_at':str(user.created_at)
                }
                
                data = CreateUserResponseSerilizer(
                    user=user_data,
                    token=access_token,
                    refresh_token=refresh_token,
                )
                serializer = SuccessResponseSerializer(
                    code=status.HTTP_200_OK,
                    message='User Created SuccessFully ...',
                    data=data
                )
                
                response = response_structure(
                    serializer=serializer,
                    status_code=status.HTTP_200_OK
                )

        except Exception as e:
            serializer = ErrorResponseSerializer(
                    code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message=f'Error : {e}',
                    data=None
                )
                
            response = response_structure(
                serializer=serializer,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response
    
    
    @classmethod
    async def update_user(cls,token:Request,name,user_name,email,phone_number,dob,profile_image,authorize):
        await auth_check(Authorize=authorize, token=token)
        try:
        
            user_id = authorize.get_jwt_subject()
            
            data = await UserProfileSchema.update_profile(
                user_id=user_id,
                name=name,
                user_name=user_name,
                email=email,
                phone_number=phone_number,
                dob=dob,
                profile_image=profile_image,
            )
            
            serializer = SuccessResponseSerializer(
                    code=status.HTTP_200_OK,
                    message='User Profile Updated',
                )
                
            response = response_structure(
                serializer=serializer,
                status_code=status.HTTP_200_OK
            )
            
        except Exception as e:
            if 'user_user_name_key' in str(e):
                message = "Username already Taken"
            elif 'user_phone_number_key' in str(e):
                message = "Phone number already exists. Please use a different phone number."
            elif 'user_email_key' in str(e):
                message = "Email already exists. Please use a different Email."
            else:
                message = f'Error : {str(e)}'
                
            serializer = ErrorResponseSerializer(
                    code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message=message,
                    data=None
                )
                
            response = response_structure(
                serializer=serializer,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response

    @classmethod
    async def check_username(cls,user_name):
        user = await UserSchema.get_user(user_name=user_name)
        if user:
            return False
        else:
            return True
        

    @classmethod
    async def suggest_usernames(cls,token:Request,user_name,authorize):
        await auth_check(Authorize=authorize,token=token)
        user_id = authorize.get_jwt_subject()
        try:

            availability = await cls.check_username(user_name=user_name)

            if availability:
                serializer = SuccessResponseSerializer(
                        code=status.HTTP_404_NOT_FOUND,
                        message='Available',
                    )
                    
                response = response_structure(
                    serializer=serializer,
                    status_code=status.HTTP_404_NOT_FOUND
                )
                
            else:
                
                suggestions =  await UserSchema.suggest_usernames(user_id=user_id,user_name=user_name)

                print(f"\n\n\n suggestions { suggestions } \n\n\n")

                serializer = SuccessResponseSerializer(
                        code=status.HTTP_200_OK,
                        message='Not Available check suggested user_name list',
                        data=suggestions
                    )
                    
                response = response_structure(
                    serializer=serializer,
                    status_code=status.HTTP_200_OK
                )
                
        except Exception as e:
            serializer = ErrorResponseSerializer(
                    code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message=f'Error : --> {str(e)}',
                    data=None
                )
                
            response = response_structure(
                serializer=serializer,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response
    
    @classmethod
    async def search_user(cls,token:Request,search_term,authorize):
        await auth_check(Authorize=authorize,token=token)
        try:
            searched_users = await UserSchema.search_user(search_term=search_term)
            if searched_users != []:
                user_data = [
                    {
                        'id': user.id,
                        'name':user.name,
                        'user_name':user.user_name,
                        'profile_image':user.profile_image,
                    } for user in searched_users
                ]
                
                serializer = SuccessResponseSerializer(
                        code=status.HTTP_200_OK,
                        message='Get Searched User Profile Data',
                        data = user_data
                    )
                    
                response = response_structure(
                    serializer=serializer,
                    status_code=status.HTTP_200_OK
                )
            else:
                serializer = SuccessResponseSerializer(
                        code=status.HTTP_404_NOT_FOUND,
                        message='Searched User Not Found',
                    )
                    
                response = response_structure(
                    serializer=serializer,
                    status_code=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            serializer = ErrorResponseSerializer(
                    code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message=f'Error : --> {str(e)}',
                    data=None
                )
                
            response = response_structure(
                serializer=serializer,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response
            
            
            
            
