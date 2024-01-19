from jose import jwt
from fastapi import HTTPException,status
from dotenv import load_dotenv
import os

load_dotenv()

AUTHJWT_SECRET_KEY = os.getenv("AUTHJWT_SECRET_KEY")

async def auth_check(Authorize, token):
    if token.headers.get("Authorization"):
        jwt_token = token.headers.get("Authorization")
        token_prefix = "Bearer "

        if jwt_token.startswith(token_prefix):
            jwt_token = jwt_token[len(token_prefix):]

            try:
                payload = jwt.decode(jwt_token, AUTHJWT_SECRET_KEY, algorithms=["HS256"],options={'verify_signature':False})
                # Optionally, you can do additional checks on the payload here

            except jwt.ExpiredSignatureError:
                raise HTTPException(
                    detail='Token Expired!',
                    status_code=status.HTTP_403_FORBIDDEN
                )
            except jwt.JWTError as e:
                raise HTTPException(
                detail=f'Invalid Token: {str(e)}',
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        else:
            raise HTTPException(
                detail='Invalid Token Format!',
                status_code=status.HTTP_401_UNAUTHORIZED
            )
    else:
        raise HTTPException(
            detail='Token Missing!',
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(
            detail='Please log in to access this page.',
            status_code=status.HTTP_401_UNAUTHORIZED
        )