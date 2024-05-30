from QIT.serializers import GenerateOTPSerializer,UserSerializer
from rest_framework.decorators import api_view,authentication_classes
from .emails import Send_OTP
from rest_framework.response import Response
import random
import string
from QIT.models import QitOtp, QitCompanymaster, QitUserlogin
import threading
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

# Custom Authentication class
class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user = authenticate(request)
        if user is None:
            raise AuthenticationFailed('Authentication failed')
        return (user, None) 

def authenticate(request):
    token = request.headers.get('Authorization', None)
    if not token:
        return None
    try:
        token = token.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token.payload['user_id']
        user = QitUserlogin.objects.get(transid=user_id)
        return user
    except Exception as e:
        return None

# Generate OTP function
def generate_otp():
    otp = ''.join(random.choices(string.digits, k=6))
    return otp

# Generate OTP API
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


# Verify OTP API
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
    
# Refresh Token API
@api_view(['POST'])
def token_refresh(request):
    refresh_token = request.data
    if refresh_token['refresh_token']:
        try:
            refresh = RefreshToken(refresh_token['refresh_token'])
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

# Login API with refresh and access token
@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = QitUserlogin.objects.get(useremail=email)
        if user and check_password(password, user.password):
            if user is not None:
                refresh = RefreshToken.for_user(user)
                user_serializer = UserSerializer(user)

                return Response({
                    'user': user_serializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except QitUserlogin.DoesNotExist:
        return Response({'detail': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
# Example API of authenticating an API Means how to verify access token
@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def secure_view(request):
    return Response({'message': 'This is a secured view!'})
