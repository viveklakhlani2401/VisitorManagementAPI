from django.core.mail import send_mail
from QIT.settings import EMAIL_HOST_USER

def Send_OTP(email, subject, message):
    try:
        send_mail(subject, message, EMAIL_HOST_USER, [email] )
        return True
    except Exception as e:
        return False