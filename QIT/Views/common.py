from QIT.serializers import GenerateOTPSerializer,UserSerializer
from rest_framework.decorators import api_view,authentication_classes
from .emails import Send_OTP
import random
import string
from QIT.models import QitOtp, QitCompanymaster, QitUserlogin
import threading
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.core.cache import cache
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
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
        # print(f"email thread start for {body_data["E_Mail"]}")
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
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except QitUserlogin.DoesNotExist:
        return Response({'detail': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
# Example API of authenticating an API Means how to verify access token
@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def secure_view(request):
    return Response({'message': 'This is a secured view!'})

# Create User login for ALL type of User
def create_userlogin(useremail, password, userrole):
    userlogin = QitUserlogin(useremail=useremail, password=make_password(password), userrole=userrole)
    userlogin.save()
    return userlogin

@csrf_exempt
@api_view(['POST'])
def Forget_Password_Send_OTP(request):
    try:
        body_data = request.data
        print(body_data["e_mail"])
        resDB = QitUserlogin.objects.filter(useremail = body_data["e_mail"]).first()
        if resDB is not None:
            print(resDB.userrole)
            print(resDB.userrole is "COMPANY")
        else:
            print("No user found with this email.")
        if not resDB:
            return Response({
                'Status':400,
                'StatusMsg':"Invalid User..!!"
            })
        
        if resDB.userrole == "COMPANY":
            new_OTP = generate_otp()
            # globalOTPStorage['email'] = body_data["e_mail"]
            # globalOTPStorage['otp'] = new_OTP
            set_otp(body_data["e_mail"],new_OTP)
            message = f"Forget Email OTP : {new_OTP}"
            Send_OTP(body_data["e_mail"],"Forget Email OTP",message)
            return Response({
                'Status':200,
                'StatusMsg':"Valid User..!!",
                'Role':"Company"
            })
        
        if resDB.userrole == "USER":
            return Response({
                'Status':200,
                'StatusMsg':"Valid User..!!",
                'Role':"USER"
            })
        
        if resDB.userrole == "VISITOR":
            return Response({
                'Status':200,
                'StatusMsg':"Valid User..!!",
                'Role':"VISITOR"
            })
        
    except Exception as e:
        return Response({
            'Status':400,
            'StatusMsg':e,
        })
    
# Verify OTP API
@csrf_exempt
@api_view(["POST"])
def VerifyForgetpasswordOTP(request):
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
        email = body_data["E_Mail"]
        otp = body_data["VerifyOTP"]
        stored_data_json = cache.get(f"otp_{email}")
        if stored_data_json:
            stored_data = json.loads(stored_data_json)
            stored_otp = stored_data['otp']
            if stored_otp:
                print(f"Comparing OTPs: '{stored_otp}' == '{otp}'")
                if str(stored_otp).strip() == str(otp).strip():
                    stored_data['status'] = 1
                    cache.set(f"otp_{email}", json.dumps(stored_data), timeout=300)
                    response = {
                        'Status': 200,
                        'StatusMsg': "OTP verified..!!"
                    }
                    return Response(response)
                else:
                    response = {
                        'Status': 400,
                        'StatusMsg': "Invalid OTP ..!!"
                    }
                    return Response(response)
            else:
                response = {
                    'Status': 400,
                    'StatusMsg': "Email not found or OTP expired..!!"
                }
                return Response(response)
        else:
            response = {
                    'Status': 400,
                    'StatusMsg': "Something wrong..!!"
                }
            return Response(response)
    except:
        return Response({
            'Status':400,
            'StatusMsg':"Invalid Email or OTP ..!!"
        })

def set_otp(email, otp, status=0):
    data = json.dumps({'otp': otp, 'status': status})
    cache.set(f"otp_{email}", data, timeout=300)

@csrf_exempt
@api_view(["POST"])
def generate_newPassword(request):
    try:
        body_data = request.data
        if not body_data["e_mail"]:
            return Response({'error': 'Email ID is required'}, status=400)
        if not body_data["password"]:
            return Response({'error': 'New Password is required'}, status=400)
        email = body_data["e_mail"]
        stored_data_json = cache.get(f"otp_{email}")
        if stored_data_json:
            stored_data = json.loads(stored_data_json)
            stored_status = stored_data['status']
            if stored_status == 1 :
                resDB1 = QitCompanymaster.objects.filter(e_mail = body_data["e_mail"]).first()
                resDB = QitUserlogin.objects.filter(useremail = body_data["e_mail"]).first()
                if not resDB:
                    return Response({
                        'Status':400,
                        'StatusMsg':"Invalid User..!!"
                    })
                
                if resDB.userrole == "COMPANY":
                    newPassword = make_password(body_data["password"])
                    resDB.password = newPassword
                    resDB.save()
                    resDB1.password = newPassword
                    resDB1.save()
                    return Response({
                        'Status':200,
                        'StatusMsg':"Company Password Updated..!!",
                        'Role':"Company"
                    })
                
                if resDB.userrole == "USER":
                    return Response({
                        'Status':200,
                        'StatusMsg':"Valid User..!!",
                        'Role':"USER"
                    })
                
                if resDB.userrole == "VISITOR":
                    return Response({
                        'Status':200,
                        'StatusMsg':"Valid User..!!",
                        'Role':"VISITOR"
                    })
            else:
                response = {
                    'Status': 400,
                    'StatusMsg': "OTP is not verified..!!"
                }
                return Response(response)
        else:
            response = {
                    'Status': 400,
                    'StatusMsg': "Email not found or OTP expired..!!"
                }
            return Response(response)
    except Exception as e:
        return Response({
            'Status':400,
            'StatusMsg':e,
        })

# for testing websocket
@csrf_exempt
@api_view(['GET'])
def getWebsocketTest(request):
    user_ids = request.GET.getlist('user_ids[]')  # Retrieving list of user IDs from query parameters
    message = "Hello"  # Message to be sent

    channel_layer = get_channel_layer()
    for user_id in user_ids:
        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {
                'type': 'send.message',
                'text': message,
            }
        )

    return Response({"status": True}, status=status.HTTP_200_OK)