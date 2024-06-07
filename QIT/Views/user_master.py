from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from QIT.models import QitUsermaster,QitUserlogin,QitCompany
from QIT.serializers import QitUsermasterSerializer,UserMasterDataSerializer,UserMasterResetSerializer
from .common import create_userlogin,create_comp_auth
from django.contrib.auth.hashers import make_password
import json
from django.core.cache import cache
from .common import set_otp,generate_otp
from .emails import Send_OTP

# @api_view(["POST"])
# def Company_User_GenerateOTP(request):
#     try:
#         if not request.data:
#             return Response({
#                 'Status':400,
#                 'StatusMsg':"e_mail is required..!!"
#             },status=400)
#         body_data = request.data["e_mail"]
#         if not body_data:
#             return Response({
#                 'Status':400,
#                 'StatusMsg':"e_mail is required..!!"
#             },status=200)
#         new_OTP = generate_otp()
#         set_otp(body_data,new_OTP)
#         message = f"New User Email OTP : {new_OTP}"
#         Send_OTP(body_data,"New User Email OTP",message)
#         return Response({
#             'Status':200,
#             'StatusMsg':f"OTP send successfully on email : {body_data}..!!"
#         },status=200)
#     except Exception as e:
#         return Response({
#             'Status':400,
#             'StatusMsg':str(e)
#         },status=400)

@api_view(['POST'])
def save_user(request):
    try:
        body_data = request.data
        stored_data_json = cache.get(f"otp_{body_data["e_mail"]}")
        if stored_data_json:
            stored_data = json.loads(stored_data_json)
            stored_status = stored_data['status']
            stored_role = stored_data['role']
            if stored_status == 1 and stored_role.upper() == "USER" :
                serializer = QitUsermasterSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    userlogin = QitUserlogin(e_mail=body_data["e_mail"], password=make_password(body_data["password"]), userrole=body_data["usertype"].upper())
                    create_comp_auth(serializer.data["transid"],QitCompany.objects.filter(transid=serializer.data["cmptransid"]).first(),body_data["usertype"].upper())
                    userlogin.save()
                    return Response({
                        'Status':status.HTTP_201_CREATED,
                        'StatusMsg':"User Save Successfully..!!"
                    }, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
            'StatusMsg':str(e)
        })

@api_view(['GET'])
def get_user(request,cmpId):
    try:
        users = QitUsermaster.objects.filter(cmptransid=cmpId)
        serializer = QitUsermasterSerializer(users, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({
                    'Status':400,
                    'StatusMsg':str(e)
                })

@api_view(['GET'])
def get_user_by_id(request, cmpId, transid):
    try:
        user = QitUsermaster.objects.get(cmptransid=cmpId, transid=transid)
    except QitUsermaster.DoesNotExist:
        return Response({'Status': 404, 'StatusMsg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserMasterDataSerializer(user)
    return Response(serializer.data)
 
@api_view(['PUT'])
def update_user(request,cmpId, transid):
    try:
        user = QitUsermaster.objects.get(cmptransid=cmpId, transid=transid)
    except QitUsermaster.DoesNotExist:
        return Response({
                    'Status':status.HTTP_404_NOT_FOUND,
                    'StatusMsg':"No data found..!!"
                },status=status.HTTP_404_NOT_FOUND)
    serializer = QitUsermasterSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
                'Status':status.HTTP_404_NOT_FOUND,
                'StatusMsg':"User Data Updated!!"
            },status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT'])
# def reset_user_password(request,cmpId, transid):
#     try:
#         user = QitUsermaster.objects.get(cmptransid=cmpId, transid=transid)
#     except QitUsermaster.DoesNotExist:
#         return Response({
#                     'Status':status.HTTP_404_NOT_FOUND,
#                     'StatusMsg':"No data found..!!"
#                 },status=status.HTTP_404_NOT_FOUND)
#     serializer = UserMasterResetSerializer(user, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({
#                 'Status':status.HTTP_404_NOT_FOUND,
#                 'StatusMsg':"User Data Updated!!"
#             },status=status.HTTP_404_NOT_FOUND)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_user(request, cmpId, transid):
    try:
        user = QitUsermaster.objects.get(cmptransid=cmpId, transid=transid)
    except QitUsermaster.DoesNotExist:
        return Response({
                    'Status':status.HTTP_404_NOT_FOUND,
                    'StatusMsg':"No data found..!!"
                },status=status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response({
                    'Status':200,
                    'StatusMsg':"User Data Deleted!!"
                })
