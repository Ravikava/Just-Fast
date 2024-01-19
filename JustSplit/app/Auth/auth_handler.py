import time
from typing import Dict
# from api.user.serializer import TokenResponseSerializer
import jwt

from app.config import config
from fastapi import Request,HTTPException
from app.db.models import User
from datetime import datetime,timedelta

JWT_SECRET = config.authjwt_secret_key
JWT_ALGORITHM = config.algorithm


def token_response(token: str):
    return {
        "access_token": token
    }

# function used for signing the JWT string
def create_access_token(user_id: int) -> Dict[str, int]:
    payload = {
        "user_id": user_id,
        "expires": datetime.today().day + 5
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print(f"\n\n\n decodeJWT RUN --- {decoded_token}\n\n\n")
        return decoded_token if decoded_token["expires"] >= datetime.today().day else None
    except Exception as e:
        print(e)
        return str(e)
    
def verify_token(req:Request):
    print("\n\n\n verify_token RUN \n\n\n")
    token = req.headers["Authorization"]
    print(f"\n\n\n token RUN --- {token}\n\n\n")
    token = token.split('Bearer')[1].strip()
    print(f"\n\n\n token RUN --- {token}\n\n\n")
    user_id = decodeJWT(str(token))
    print(f"got f_id",user_id)
    return user_id['user_id']

def get_current_user(user_id,db):
    print("hi------------------------")
    # user = db.query(User).filter(User.id == firbase_uid).first()
    print('user')
    return 'user'
    

            


    
    

    # try:
    #     payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    #     firebase_uid: str = payload.get("sub")
    #     if firebase_uid is None:
    #         raise credentials_exception
    #     token_data = TokenResponseSerializer(firebase_uid=firebase_uid)
    # except JWTError:
    #     raise credentials_exception
    
