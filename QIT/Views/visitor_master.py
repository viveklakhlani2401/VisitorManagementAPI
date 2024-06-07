from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from QIT.models import QitUserlogin
# from QIT.serializers import QitUsermasterSerializer,UserMasterDataSerializer,UserMasterResetSerializer
# from .common import create_userlogin,create_comp_auth
# from django.contrib.auth.hashers import make_password
# import json
# from django.core.cache import cache
from .common import set_otp,generate_otp
from .emails import Send_OTP

# @api_view(["POST"])
# def Visitor_GenerateOTP(request):
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
#         userEntry = QitUserlogin.objects.filter(e_mail=body_data).first()
#         if userEntry:
#             return Response({
#                 'Status':400,
#                 'StatusMsg':"User with this email already exists..!!"
#             },status=400)
#         new_OTP = generate_otp()
#         set_otp(body_data,new_OTP)
#         message = f"Visitor OTP : {new_OTP}"
#         Send_OTP(body_data,"Visitor OTP",message)
#         return Response({
#             'Status':200,
#             'StatusMsg':f"OTP send successfully on email : {body_data}..!!"
#         },status=200)
#     except Exception as e:
#         return Response({
#             'Status':400,
#             'StatusMsg':str(e)
#         },status=400)

