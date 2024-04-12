from sqlalchemy.future import select
from app.db.models import User,UserLogin
from app.db.database import db
from sqlalchemy import update
from datetime import datetime
from app.config.config import S3Config

import random
class UserSchema:
    
    @classmethod
    async def test_data(cls,user_id):
        data = select(
            User
        ).where(User.id == user_id)
        data = await db.execute(data)
        data = data.scalars().first()
        return data
    
    @classmethod
    async def get_user(cls,email = None,user_id = None,phone_number = None,user_name=None):
        if email:
            filter = User.email == email
        if user_id:
            filter = User.id == int(user_id)
        if phone_number:
            filter = User.phone_number == phone_number
        if user_name:
            filter = User.user_name == user_name
        data = select(
            User
        ).where(filter)
        data = await db.execute(data)
        data = data.scalars().first()
        return data
    
    @classmethod
    async def update_devices(cls,user_id,value_dict):
        device = update(
            User
        ).where(
            User.id == user_id
        ).values(
            value_dict
        ).execution_options(
            synchronize_session="fetch"
        )
        await db.execute(device)
        
        try:
            await db.commit()
        except:
            await db.rollback()
        return True
    
    @classmethod
    async def add_device_login_details(cls,user,device_id,device_name):
        device_details = UserLogin(
                    user_id = user.id,
                    device_id = device_id,
                    device_name = device_name,
                    logged_in_status = True,
                    login_at = datetime.now()
                )
                
        db.add(device_details)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
        return device_details
    
    @classmethod
    async def create_user(cls,name,profile_image,email,device_id):
        user = User(
            name = name,
            profile_image = profile_image,
            email = email,
            device_ids = [device_id],
            current_currency = "INR"
        )
        db.add(user)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
        
        return user
            
    @classmethod
    async def update_user(cls,user_id,value_dict):
        
        if value_dict.get('dob'):
            user = await cls.get_user(user_id=user_id)
            if user.dob != None:
                value_dict.pop('dob')
            
        user = update(
            User
        ).where(
            User.id == int(user_id)
        ).values(
            value_dict
        ).execution_options(
            synchronize_session="fetch"
        )
        await db.execute(user)
        try:
            await db.commit()
        except:
            await db.rollback()
        return True
    
    @classmethod
    async def suggest_usernames(cls,user_id,user_name):
        suggestions = []
        user = await cls.get_user(user_id=user_id)
                
        if user.name != None or user.name != '':
                if ' ' in user.name:
                    name = user.name.split(' ')
                else:
                    name = None
        email = user.email.split('@')
        if name:
            suggestions.append(f"{name[0].lower()}{name[1].lower()}")
        suggestions.append(f"{email[0]}")
        
        if name:
            if len(name) >= 2:
                first_name, last_name = name[0], name[-1]
                suggestions.append(f"{last_name[0].lower()}{first_name.lower()}")
                suggestions.append(f"{first_name.lower()}{last_name[0].lower()}")
            
        for _ in range(4):
            randon_number = random.randint(111,999)
            numbered_username = f"{user_name}{randon_number}"
            suggestions.append(numbered_username)
        
        for user_name in suggestions:
            exists = await cls.get_user(user_name=user_name)
            
            if exists:
                suggestions.remove(exists.user_name)
        return suggestions
    
    @classmethod
    async def search_user(cls,search_term):
        filter_condition = (
            (User.name.ilike(f'%{search_term}%')) |
            (User.email.ilike(f'%{search_term}%')) |
            (User.user_name.ilike(f'%{search_term}%')) |
            (User.phone_number.ilike(f'{search_term}%'))
        )
        
        data = select(User).where(filter_condition)
        data = await db.execute(data)
        user_data = data.scalars().all()
        
        return user_data
        
    


class UserProfileSchema:    
    
    @classmethod
    async def update_profile(cls,user_id,name,user_name,email,phone_number,dob,profile_image):
        value_dict = {}
        if name:
            value_dict['name'] = name
        if user_name:
            value_dict['user_name'] = user_name
        if email:
            value_dict['email'] = email
        if phone_number:
            value_dict['phone_number'] = phone_number
        if dob:
            value_dict['dob'] = dob
        if profile_image:
            profile_image = S3Config.upload_image(profile_image)
            value_dict['profile_image'] = profile_image
        
        print(f"sending data for update --> {value_dict}")
        
        await UserSchema.update_user(
            user_id=user_id,
            value_dict=value_dict
        )
        
        user = await UserSchema.get_user(
            user_id=user_id
        )
        
        return user


