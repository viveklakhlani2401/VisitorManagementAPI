import threading
from django.core.mail import EmailMultiAlternatives,EmailMessage
from django.http import JsonResponse
from rest_framework.response import Response
from QIT.settings import EMAIL_HOST_USER
from QIT.utils.APICode import APICodeClass
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .send_email import send_html_mail

@csrf_exempt
@api_view(["POST"])
def GenerateOTP(request):
    try:
        # email = request.data["e_mail"]
        # role = request.data["role"]

        send_html_mail("My super subject","My super html content",["dhruvirana567@gmail.com"])

        # threading.Thread(
        #     target=send_html_mail,
        #     kwargs={
        #         "subject": "My super subject",
        #         "html_content": "My super html content",
        #         "recipient_list": ["dhruvirana567@gmail.com"]
        #     }
        # ).start()
        
        return Response({
            'Status': 200,
            'StatusMsg': "Email sent..!!",
            "APICode": APICodeClass.Auth_Generate_OTP.value
        }, status=200)
        
    except Exception as e:
        return Response({
            'Status': 400,
            'StatusMsg': str(e),
            "APICode": APICodeClass.Auth_Generate_OTP.value
        }, status=400)
    


import threading
from threading import Thread

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMessage(self.subject, self.html_content, EMAIL_HOST_USER, self.recipient_list)
        msg.content_subtype = "html"
        msg.send()


def send_html_mail(subject, html_content, recipient_list):
    EmailThread(subject, html_content, recipient_list).start()
