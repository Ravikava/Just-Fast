#FastAPI Imports
import os
from dotenv import load_dotenv
import boto3
import base64
import uuid
from fastapi_mail import ConnectionConfig
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from PIL import Image
from fastapi import UploadFile

load_dotenv()
class Config:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_CONFIG = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    # RAZORPAY_KEY = os.getenv("RAZORPAY_KEY", "")
    # RAZORPAY_SECRET = os.getenv("RAZORPAY_SECRET", "")
    # TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID","")
    # TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN","")
    # TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")
    # OTP_SEND = os.getenv("OTP_SEND", "False")
    # FCM_API_URL = os.getenv("FCM_API_URL")
    # FCM_SERVER_KEY = os.getenv("FCM_SERVER_KEY")
    # SHIPROCKET_URL = "https://apiv2.shiprocket.in/v1/external"
    # SHIPROCKET_EMAIL = os.getenv("SHIPROCKET_EMAIL")
    # SHIPROCKET_PASSWORD = os.getenv("SHIPROCKET_PASSWORD")
    # BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
    

class S3Config:
    
    def upload_image_to_s3(file_name, image_content, extension):
        try:
            s3_client = boto3.client(
                "s3",
                region_name=os.getenv('AWS_DEFAULT_REGION'),
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )

            # Upload object
            s3_client.put_object(Body=image_content, Bucket=os.getenv('AWS_BUCKET_NAME'),
                                ContentType=f'image/{extension}', Key=file_name)

            return file_name
        except Exception as error:
            raise error
    
    def upload_image(image: UploadFile):
        # image = request.files['image']
        # Generate file
        file_id = uuid.uuid4().hex
        image_file_extension = os.path.splitext(image.filename)[1][1:]
        file_name = f"Profile/{file_id}.{image_file_extension}"

        # Read the file content
        image_content = image.file.read()

        # Upload the file
        s3_file = S3Config.upload_image_to_s3(file_name, image_content, image_file_extension)

        image_url = f'https://{os.getenv("AWS_BUCKET_NAME")}.s3.amazonaws.com/{s3_file}'

        return image_url
    
    

    def upload_file(file_obj, object_name=None):
        """Upload a file to an S3 bucket

        :param s3_client: S3 Client
        :param file_obj: File to upload
        :param bucket: Bucket to upload to
        :param folder: Folder to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        ACCESS_KEY = os.getenv("ACCESS_KEY", "AKIA2DUJSPHWJME4CKDL")
        SECRET_KEY = os.getenv("SECRET_KEY", "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")
        S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "stash-out")
        # region_name=config('AWS_DEFAULT_REGION'), 

        s3_client = boto3.client("s3", 
                    aws_access_key_id=ACCESS_KEY, 
                    aws_secret_access_key=SECRET_KEY)
        # If S3 object_name was not specified, use file_name

        if object_name is None:
            object_name = file_obj
        try:
            s3_client.upload_file(file_obj, S3_BUCKET_NAME, f"media/{object_name}",ExtraArgs = {
                "ContentType": 'image/png',
                'ACL':'public-read'
            })
        except Exception as e:
            print("printing exception")
            print(e)
            return False
        return True
    
    def img_conversion(img_data,object_name=None):
        decode_data = base64.b64decode(img_data)
        img_file = open(f'./{object_name}.png','wb')
        img_file.write(decode_data)
        img_file.close()
        if object_name is None:
            object_name=f'{uuid.uuid4()}'
        default_image = Image.open(f'./{object_name}.png')
        image_256x256 = default_image.resize((256,256))
        image_512x512 = default_image.resize((512,512))
        image_1024x1024 = default_image.resize((1024,1024))
        image_256x256.save(f'{object_name}_256x256.png')
        image_512x512.save(f'{object_name}_512x512.png')
        image_1024x1024.save(f'{object_name}_1024x1024.png')
        check = True
        if check:
            check = S3Config.upload_file(file_obj=f'{object_name}.png',object_name=f'{object_name}.png')
        if check:
            check = S3Config.upload_file(file_obj=f'{object_name}_256x256.png',object_name=f'{object_name}_256x256.png')
        if check:
            check = S3Config.upload_file(file_obj=f'{object_name}_512x512.png',object_name=f'{object_name}_512x512.png')
        if check:
            check = S3Config.upload_file(file_obj=f'{object_name}_1024x1024.png',object_name=f'{object_name}_1024x1024.png')
        os.remove(f'./{object_name}.png')
        os.remove(f'./{object_name}_256x256.png')
        os.remove(f'./{object_name}_512x512.png')
        os.remove(f'./{object_name}_1024x1024.png')

conf = ConnectionConfig(
   MAIL_USERNAME = os.getenv("MAIL_USERNAME", ""),
   MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", ""),
   MAIL_PORT = 587,
   MAIL_SERVER = "smtp.gmail.com",
   MAIL_STARTTLS = True,
   MAIL_SSL_TLS = False,
   USE_CREDENTIALS = True,
   VALIDATE_CERTS = True,
   MAIL_FROM = os.getenv("MAIL_USERNAME", "")
)


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"

@AuthJWT.load_config
def get_config():
    return Settings()

authjwt_secret_key="cddbedfd8cc5b5395ba619d838d76d75"
algorithm='HS256'