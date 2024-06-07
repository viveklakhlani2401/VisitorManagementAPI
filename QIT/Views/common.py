from QIT.serializers import GenerateOTPSerializer,UserSerializer
from rest_framework.decorators import api_view,authentication_classes
from .emails import Send_OTP
import random
import string
from QIT.models import QitOtp, QitCompany, QitUserlogin,QitAuthenticationrule,QitUsermaster
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
from QIT.utils import modules
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
    try:
        if not request.data:
            return Response({
                'Status':400,
                'StatusMsg':"Payload is required..!!"
            },status=400)
        email = request.data["e_mail"]
        role = request.data["role"]
        if not email:
            return Response({
                'Status':400,
                'StatusMsg':"e_mail is required..!!"
            },status=200)
        if not role:
            return Response({
                'Status':400,
                'StatusMsg':"role is required..!!"
            },status=200)
        
        userEntry = QitUserlogin.objects.filter(e_mail=email).first()
        if userEntry:
            return Response({
                'Status':400,
                'StatusMsg':"User with this email already exists..!!"
            },status=400)
        new_OTP = generate_otp()
        if role.upper() == "COMPANY":
            message = f"Company OTP : {new_OTP}"
        elif role.upper() == "VISITOR":
            message = f"Visitor OTP : {new_OTP}"
        elif role.upper() == "USER":
            message = f"User OTP : {new_OTP}"
        else:
            return Response({
                'Status':400,
                'StatusMsg':"Invalid role..!!"
            },status=400)


        set_otp(email,new_OTP,role.upper())
        Send_OTP(email,f"{role.upper()} OTP",message)
        return Response({
            'Status':200,
            'StatusMsg':f"OTP send successfully on email : {email}..!!"
        },status=200)
    except Exception as e:
        return Response({
            'Status':400,
            'StatusMsg':str(e)
        },status=400)
    


# @csrf_exempt
# @api_view(["POST"])
# def GenerateOTP(request):
#     body_data = request.data
#     new_OTP = generate_otp()

#     try:
#         if not body_data.get("E_Mail"):
#             return Response({
#                 'Status':400,
#                 'StatusMsg':"Email is required..!!"
#             })
#         print("first check in comapny master")
#         emailExistInComapny = QitCompany.objects.filter(e_mail = body_data["E_Mail"])
#         if(emailExistInComapny):
#             return Response({
#                 'Status':400,
#                 'StatusMsg':"This email alredy register as comapny..!!"
#             })
#         # try:
#         #     print("first check in otp master")
#         #     OTPEntry = QitOtp.objects.get(e_mail = body_data["E_Mail"])
#         #     print(OTPEntry)
#         #     OTPEntry.verifyotp = new_OTP
#         #     OTPEntry.status = "N"
#         #     # OTPEntry.entrytime = timezone.now()
#         #     print(f"OTP while save : {new_OTP}")
#         #     OTPEntry.save()
#         # except QitOtp.DoesNotExist :
#         #     print("finally here")
#         #     print(f"OTP while create : {new_OTP}")
#         #     OTPEntry = QitOtp.objects.create(e_mail = body_data["E_Mail"],verifyotp = new_OTP, status = "N")
#         set_otp(body_data["E_Mail"],new_OTP)
#         message = "OTP : "+new_OTP
#         Send_OTP(body_data["E_Mail"],"TEST",message)
#         return Response({
#             'Status':200,
#             'StatusMsg':"OTP send successfully..!!"
#         })
#     except Exception as e:
#         return Response({
#             'Status': 400,
#             'StatusMsg': "Error while sending OTP: " + str(e)
#         })

#     # if(OTPEntry):
#     #     message = "OTP : "+new_OTP
#     #     # email_thread = threading.Thread(target=Send_OTP,args=(body_data["E_Mail"],"TEST",message))
#     #     # email_thread.start()
#     #     # print(f"email thread start for {body_data["E_Mail"]}")
#     #     print(f"message {message}")
#     #     Send_OTP(body_data["E_Mail"],"TEST",message)
#     #     return Response({
#     #         'Status':200,
#     #         'StatusMsg':"OTP send successfully..!!"
#     #     })
    
#     # return Response({
#     #     'Status':400,
#     #     'StatusMsg':"Error while sending OTP..!!"
#     # })


# Verify OTP API
@csrf_exempt
@api_view(["POST"])
def VerifyOTP(request):
    body_data = request.data
    try:
        if not body_data:
            return Response({
                'Status':400,
                'StatusMsg':"Payload is required..!!"
            })
        if not body_data.get("e_mail"):
            return Response({
                'Status':400,
                'StatusMsg':"Email is required..!!"
            })
        if not body_data.get("VerifyOTP"):
            return Response({
                'Status':400,
                'StatusMsg':"OTP is required..!!"
            })
        if not body_data.get("role"):
            return Response({
                'Status':400,
                'StatusMsg':"Role is required..!!"
            })
        
        email = body_data.get("e_mail")
        otp = body_data.get("VerifyOTP")
        role = body_data.get("role")
        stored_data_json = cache.get(f"otp_{email}")
        if stored_data_json:
            stored_data = json.loads(stored_data_json)
            stored_otp = stored_data['otp']
            stored_role = stored_data['role']
            if stored_otp:
                print(f"Comparing OTPs: '{stored_otp}' == '{otp}'")
                print(f"Comparing OTPs: '{stored_role}' == '{role}'")
                if str(stored_otp).strip() == str(otp).strip() and stored_role.upper() == role.upper():
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
        # OTPEntry = QitOtp.objects.get(e_mail = body_data["E_Mail"], verifyotp = body_data["VerifyOTP"])
        # if(OTPEntry.status == "Y"):
        #     return Response({
        #         'Status':200,
        #         'StatusMsg':"OTP already veryfied..!!"
        #     })
        # print(timezone.now())
        # print(OTPEntry.entrytime)
        # time_difference = timezone.now() - OTPEntry.entrytime
        # if time_difference.total_seconds() > 300:  # 5 minutes = 300 seconds
        #     return Response({
        #         'Status': 400,
        #         'StatusMsg': "OTP has expired..!!"
        #     })
        # OTPEntry.status = "Y"
        # OTPEntry.save()
        # return Response({
        #     'Status':200,
        #     'StatusMsg':"OTP veryfied..!!"
        # })
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
# @api_view(['POST'])
# def login_view(request):
#     email = request.data.get('email')
#     password = request.data.get('password')
#     try:
#         user = QitUserlogin.objects.get(e_mail=email)
#         print(check_password(password, user.password))
#         if user and check_password(password, user.password):
#             print("here")
#             if user is not None:
#                 print("here")
#                 user_serializer = UserSerializer(user)
#                 print("here",user_serializer.data)
#                 refresh = RefreshToken.for_user(user)

#                 return Response({
#                     'user': user_serializer.data,
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                 })
#             else:
#                 return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#     except QitUserlogin.DoesNotExist:
#         return Response({'detail': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)


def role_email_wise_data(e_mail,password,role):
    print("===========")
    print(e_mail,password,role)
    if role == "COMPANY":
        user = QitCompany.objects.filter(e_mail=e_mail).first()
        if user and check_password(password, user.password):
            return user
        else:
            return None
    elif role == "USER":
        print("__________")
        user = QitUsermaster.objects.filter(e_mail=e_mail).first()
        print(user)
        if user and check_password(password, user.password):
            return user
        else:
            return None
    elif role == "ADMIN":
        user = QitUsermaster.objects.filter(e_mail=e_mail,usertype=role.upper()).first()
        if user and check_password(password, user.password):
            return user
        else:
            return None
 
# Login API with refresh and access token
@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = QitUserlogin.objects.get(e_mail=email)
        print(check_password(password, user.password))
        if user and check_password(password, user.password):
            print("here")
            if user is not None:
                print("here")
                user_serializer = UserSerializer(user)
                print("here",user_serializer.data)
                refresh = RefreshToken.for_user(user)
                chkUser  = role_email_wise_data(email,password,user.userrole)
                print(chkUser)
                if chkUser == None:
                    return Response({'detail': 'Something wrong'}, status=status.HTTP_404_NOT_FOUND)
                obj = QitAuthenticationrule.objects.filter(user_id=chkUser.transid).first()
                # obj = QitAuthenticationrule.objects.all()
                # obj_list = list(obj.values())
        
                json_text = json.dumps(obj.auth_rule_detail)
                
                # Encrypt the serialized data
                # key = b'your_secret_key_here'  # Replace with your secret key
                # cipher_suite = Fernet(key)
                # encrypt_bytes = cipher_suite.encrypt(json_text.encode())
 
                return Response({
                    'user': user_serializer.data,
                    'userAuth':json_text,
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
    userlogin = QitUserlogin(e_mail=useremail, password=make_password(password), userrole=userrole)
    userlogin.save()
    return userlogin

def create_comp_auth(useremail, cmptransid, userrole):
    print("=============> ",useremail," ", cmptransid," ", userrole)
    modulesdata = None
    if userrole == "COMPANY":
        modulesdata = modules.module_classes
    elif userrole == "USER":
        modulesdata = modules.user_module_classes
    elif userrole == "ADMIN":
        modulesdata = modules.module_classes
    compuserauth = QitAuthenticationrule(user_id=useremail,cmptransid=cmptransid, userrole=userrole,auth_rule_detail=modulesdata)
    compuserauth.save()
    return compuserauth

@csrf_exempt
@api_view(['POST'])
def Forget_Password_Send_OTP(request):
    try:
        body_data = request.data
        resDB = QitUserlogin.objects.filter(useremail = body_data["e_mail"]).first()
        if resDB is not None:
            print(resDB.userrole)
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
            set_otp(body_data["e_mail"],new_OTP,"COMPANY")
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
# @csrf_exempt
# @api_view(["POST"])
# def VerifyOTP(request):
#     body_data = request.data

#     try:
#         if not body_data :
#             return Response({
#                 'Status':400,
#                 'StatusMsg':"Payload is required..!!"
#             },status=400)
#         if not body_data["e_mail"]:
#             return Response({
#                 'Status':400,
#                 'StatusMsg':"Email is required..!!"
#             })
#         if not body_data["VerifyOTP"]:
#             return Response({
#                 'Status':400,
#                 'StatusMsg':"OTP is required..!!"
#             })
#         email = body_data["e_mail"]
#         otp = body_data["VerifyOTP"]
#         print(email)
#         print(otp)
#         stored_data_json = cache.get(f"otp_{email}")
#         print(stored_data_json)
#         if stored_data_json:
#             stored_data = json.loads(stored_data_json)
#             stored_otp = stored_data['otp']
#             if stored_otp:
#                 print(f"Comparing OTPs: '{stored_otp}' == '{otp}'")
#                 if str(stored_otp).strip() == str(otp).strip():
#                     stored_data['status'] = 1
#                     cache.set(f"otp_{email}", json.dumps(stored_data), timeout=300)
#                     response = {
#                         'Status': 200,
#                         'StatusMsg': "OTP verified..!!"
#                     }
#                     return Response(response)
#                 else:
#                     response = {
#                         'Status': 400,
#                         'StatusMsg': "Invalid OTP ..!!"
#                     }
#                     return Response(response)
#             else:
#                 response = {
#                     'Status': 400,
#                     'StatusMsg': "Email not found or OTP expired..!!"
#                 }
#                 return Response(response)
#         else:
#             response = {
#                     'Status': 400,
#                     'StatusMsg': "Something wrong..!!"
#                 }
#             return Response(response)
#     except:
#         return Response({
#             'Status':400,
#             'StatusMsg':"Invalid Email or OTP ..!!"
#         })

def set_otp(email, otp,urole, status=0 ):
    data = json.dumps({'otp': otp, 'status': status, 'role':urole})
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
                resDB1 = QitCompany.objects.filter(e_mail = body_data["e_mail"]).first()
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