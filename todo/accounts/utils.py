from django.core.mail import EmailMessage
import os
from dotenv import load_dotenv

class Util:
    @staticmethod
    def send_email(data):
        load_dotenv()
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.getenv('EMAIL_HOST_USER'),
            to=[data['to_email']]
        )
        email.send()