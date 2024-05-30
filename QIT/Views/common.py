from QIT.serializers import GenerateOTPSerializer
from rest_framework.decorators import api_view
from .emails import Send_OTP
from rest_framework.response import Response
import random
import string
from QIT.models import QitOtp, QitCompanymaster, QitUserlogin
import threading
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.hashers import make_password

@csrf_exempt
@api_view(["POST"])
def GenerateOTP(request):
    body_data = request.data
    new_OTP = generate_otp()

    try:
        if not body_data["E_Mail"]:
            return Response({
                'Status':400,
                'StatusMsg':"Email is required..!!"
            })
        print("first check in comapny master")
        
        emailExistInComapny = QitCompanymaster.objects.filter(e_mail = body_data["E_Mail"])

        if(emailExistInComapny):
            return Response({
                'Status':400,
                'StatusMsg':"This email alredy register as comapny..!!"
            })
        
        try:
            print("first check in otp master")
            OTPEntry = QitOtp.objects.get(e_mail = body_data["E_Mail"])
            print(OTPEntry)
            OTPEntry.verifyotp = new_OTP
            OTPEntry.status = "N"
            # OTPEntry.entrytime = timezone.now()
            print(f"OTP while save : {new_OTP}")
            OTPEntry.save()

 

        except QitOtp.DoesNotExist :
            print("finally here")
            print(f"OTP while create : {new_OTP}")
            OTPEntry = QitOtp.objects.create(e_mail = body_data["E_Mail"],verifyotp = new_OTP, status = "N")
    except Exception as e:
        return Response({
            'Status': 400,
            'StatusMsg': "Error while sending OTP: " + str(e)
        })   

        

    if(OTPEntry):
        message = "OTP : "+new_OTP
        # email_thread = threading.Thread(target=Send_OTP,args=(body_data["E_Mail"],"TEST",message))
        # email_thread.start()
        print(f"email thread start for {body_data["E_Mail"]}")
        print(f"message {message}")
        Send_OTP(body_data["E_Mail"],"TEST",message)
        return Response({
            'Status':200,
            'StatusMsg':"OTP send successfully..!!"
        })
    
    return Response({
        'Status':400,
        'StatusMsg':"Error while sending OTP..!!"
    })

def generate_otp():
    otp = ''.join(random.choices(string.digits, k=6))
    return otp

@csrf_exempt
@api_view(["POST"])
def VerifyOTP(request):
    body_data = request.data

    try:
        if not body_data["E_Mail"]:
            return Response({
                'Status':400,
                'StatusMsg':"Email is required..!!"
            })
        if not body_data["VerifyOTP"]:
            return Response({
                'Status':400,
                'StatusMsg':"OTP is required..!!"
            })

        OTPEntry = QitOtp.objects.get(e_mail = body_data["E_Mail"], verifyotp = body_data["VerifyOTP"])
        
        if(OTPEntry.status == "Y"):
            return Response({
                'Status':200,
                'StatusMsg':"OTP already veryfied..!!"
            })
        
        time_difference = timezone.now() - OTPEntry.entrytime
        if time_difference.total_seconds() > 300:  # 5 minutes = 300 seconds
            return Response({
                'Status': 400,
                'StatusMsg': "OTP has expired..!!"
            })
        
        OTPEntry.status = "Y"
        OTPEntry.save()
        
        return Response({
            'Status':200,
            'StatusMsg':"OTP veryfied..!!"
        })
    except QitOtp.DoesNotExist:
        return Response({
            'Status':400,
            'StatusMsg':"Invalid Email or OTP ..!!"
        })
    

def create_userlogin(useremail, password, userrole):
    userlogin = QitUserlogin(useremail=useremail, password=make_password(password), userrole=userrole)
    userlogin.save()
    return userlogin    