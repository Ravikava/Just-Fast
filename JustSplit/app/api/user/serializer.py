from pydantic import BaseModel,EmailStr,constr
from typing import Optional,List,Any


class UserResponseSerializer(BaseModel):
    id:Optional[int]
    name:Optional[str]
    user_name:Optional[str]
    profile_image: Optional[str]
    email:Optional[EmailStr]
    phone_number:Optional[str]
    dob:Optional[str]
    friends:Optional[List[int]]
    Group:Optional[List[int]]
    current_currency:Optional[str]
    all_currency_used:Optional[List[str]]
    device_ids:Optional[List[str]]
    created_at:Optional[str]


class EmailVerificationSerializer(BaseModel):
    recipient: EmailStr
    subject: str

class EmailVerificationResponseSerializer(BaseModel):
    user: Any
    token: str = None
    refresh_token : str = None
    otp: int
    
class CreateUserRequestSerializer(BaseModel):
    name: constr()
    email: EmailStr
    device_id: constr()
    device_name: constr()
    
class CreateUserResponseSerilizer(BaseModel):
    user: Any
    token: str = None
    refresh_token : str = None