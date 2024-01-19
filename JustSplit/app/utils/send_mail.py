from fastapi_mail import FastMail,MessageSchema,MessageType
from app.config.config import conf

async def send_email(recipient,subject,otp):
    template = f"""
            <html>
            <body>
            <p>
                <br>
                <p>Hi,</p>
                <br>
                <br>Here's your OTP: <{otp}></p>
                <p><b>Please use this code to complete your verification </b></p>
                <br>
                <br>
                <p>Best Regards</p>
                <br>
                <p> Just Split </p>
            </body>
            </html>
            """
    message = MessageSchema(
        subject=subject,
        recipients=[recipient],  # List of recipients, as many as you can pass  
        body=template,
        subtype=MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return True