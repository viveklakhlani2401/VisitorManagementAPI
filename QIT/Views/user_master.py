from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from QIT.models import QitUsermaster,QitUserlogin,QitCompany,QitDepartment
from QIT.serializers import QitUsermasterSerializer,UserMasterDataSerializer,UserMasterResetSerializer,UserShortDataSerializer
from .common import create_userlogin,create_comp_auth,create_comp_notification_auth

from django.contrib.auth.hashers import make_password
import json
from django.core.cache import cache
from QIT.utils.APICode import APICodeClass
    
from .template import send_credential_email
from .send_email import send_html_mail

# @api_view(["POST"])
# def Company_User_GenerateOTP(request):
#     try:
#         if not request.data:
#             return Response({
#                 'Status':400,
#                 'StatusMsg':"e_mail is required"
#             },status=400)
#         body_data = request.data["e_mail"]
#         if not body_data:
#             return Response({
#                 'Status':400,
#                 'StatusMsg':"e_mail is required"
#             },status=200)
#         new_OTP = generate_otp()
#         set_otp(body_data,new_OTP)
#         message = f"New User Email OTP : {new_OTP}"
#         Send_OTP(body_data,"New User Email OTP",message)
#         return Response({
#             'Status':200,
#             'StatusMsg':f"OTP send successfully on email : {body_data}"
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
        email = body_data["e_mail"]
        stored_data_json = cache.get(f"otp_{email}")
        if stored_data_json:
            stored_data = json.loads(stored_data_json)
            stored_status = stored_data['status']
            stored_role = stored_data['role']
            if stored_status == 1 and stored_role.upper() == "USER" :
                companyEntry = QitCompany.objects.filter(transid=body_data["cmptransid"]).first()
                if not companyEntry:
                    return Response( {
                        'isSaved':"N",
                        'Status': 400,
                        'StatusMsg': "Company not found",
                        'APICode':APICodeClass.User_Save.value
                    }, status=400)
                deptEntry = QitDepartment.objects.filter(transid=body_data["cmpdeptid"],cmptransid=companyEntry).first()
                if not deptEntry:
                    return Response( {
                        'isSaved':"N",
                        'Status': 400,
                        'StatusMsg': "Department not found",
                        'APICode':APICodeClass.User_Save.value
                    }, status=400)
                serializer = QitUsermasterSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    userlogin = QitUserlogin(e_mail=body_data["e_mail"], password=make_password(body_data["password"]), userrole=body_data["usertype"].upper())
                    create_comp_auth(serializer.data["transid"],QitCompany.objects.filter(transid=serializer.data["cmptransid"]).first(),body_data["usertype"].upper())
                    create_comp_notification_auth(serializer.data["transid"],QitCompany.objects.filter(transid=serializer.data["cmptransid"]).first(),body_data["usertype"].upper())
                    userlogin.save()
                    return Response({
                        'Status':status.HTTP_201_CREATED,
                        'StatusMsg':"User Save Successfully",
                        'APICode':APICodeClass.User_Save.value
                    }, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {
                    'Status': 400,
                    'StatusMsg': "OTP is not verified",
                    'APICode':APICodeClass.User_Save.value
                }
                return Response(response,status=400)
        else:
            response = {
                'Status': 400,
                'StatusMsg': "Email not found or OTP expired",
                'APICode':APICodeClass.User_Save.value
            }
            return Response(response,status=400)  
    except Exception as e:
        return Response({
            'Status':400,
            'StatusMsg':str(e),
            'APICode':APICodeClass.User_Save.value
        },status=400)

@api_view(['GET'])
def get_user(request,status,cmpId):
    try:
        companyEntry = QitCompany.objects.filter(transid=cmpId).first()
        if not companyEntry:
            return Response( {
                'Status': 400,
                'StatusMsg': "Company not found",
                'APICode':APICodeClass.User_Get.value
            }, status=400)
        if status.upper() == "ALL":
            users = QitUsermaster.objects.filter(cmptransid=cmpId)
            serializer = UserMasterDataSerializer(users, many=True)
            # serializer = QitUsermasterSerializer(users, many=True)
            # user_data = dict(serializer.data)
            # print(user_data)
            # user_data['dept_name'] = 2
            return Response({'Data':serializer.data,'APICode':APICodeClass.User_Get.value})
        elif status.upper() == "U":
            users = QitUsermaster.objects.filter(cmptransid=cmpId,usertype="USER")
            serializer = UserMasterDataSerializer(users, many=True)
            # serializer = QitUsermasterSerializer(users, many=True)
            return Response({'Data':serializer.data,'APICode':APICodeClass.User_Get.value})
        elif status.upper() == "A":
            users = QitUsermaster.objects.filter(cmptransid=cmpId,usertype="ADMIN")
            serializer = UserMasterDataSerializer(users, many=True)
            # serializer = QitUsermasterSerializer(users, many=True)
            return Response({'Data':serializer.data,'APICode':APICodeClass.User_Get.value})
        else:
            return Response({
                'Status': 400, 
                'StatusMsg': "Invalid state",
                'APICode':APICodeClass.User_Get.value
            }, status=400)
    except Exception as e:
        return Response({
                    'Status':400,
                    'StatusMsg':str(e),
                    'APICode':APICodeClass.User_Get.value
                },status=400)

# @api_view(['GET'])
# def get_user_by_id(request, cmpId, transid):
#     try:
#         user = QitUsermaster.objects.get(cmptransid=cmpId, transid=transid)
#     except QitUsermaster.DoesNotExist:
#         return Response({
#             'Status': 404, 
#             'StatusMsg': 'User not found',
#             'APICode':APICodeClass.User_GetById.value
#         }, status=status.HTTP_404_NOT_FOUND)
#     serializer = UserMasterDataSerializer(user)
#     return Response({
#         'Data':serializer.data,
#         'APICode':APICodeClass.User_GetById.value
#         })
 
@api_view(['GET'])
def get_user_by_id(request, cmpId, transid):
    try:
        userEntry = QitUserlogin.objects.get(transid=transid)
        user = QitUsermaster.objects.get(cmptransid=cmpId, usertype=userEntry.userrole,e_mail=userEntry.e_mail)
        serializer = UserMasterDataSerializer(user)
        return Response({
            'Data':serializer.data,
            'APICode':APICodeClass.User_GetById.value
            })
    except QitUserlogin.DoesNotExist:
        return Response({
            'Status': 404, 
            'StatusMsg': 'User not found',
            'APICode':APICodeClass.User_GetById.value
        }, status=status.HTTP_404_NOT_FOUND)
    except QitUsermaster.DoesNotExist:
        return Response({
            'Status': 404, 
            'StatusMsg': 'User not found',
            'APICode':APICodeClass.User_GetById.value
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({
            'Status':400,
            'StatusMsg':str(e),
            'APICode':APICodeClass.User_GetById.value
        },status=400)
    
 
@api_view(['PUT'])
def update_user(request):
    try:
        body_data = request.data
        if not body_data:
            return Response({'Status': 400, 'StatusMsg': "Payload required",'APICode':APICodeClass.User_Edit.value}, status=400)        
        cmpId = body_data.get("company_id")
        if not cmpId:
            return Response({'Status': 400, 'StatusMsg': "company_id required",'APICode':APICodeClass.User_Edit.value}, status=400)  
        transid = body_data.get("transid")
        if not transid:
            return Response({'Status': 400, 'StatusMsg': "transid required",'APICode':APICodeClass.User_Edit.value}, status=400)
   
        try:
            companyEntry = QitCompany.objects.get(transid=cmpId)
        except QitCompany.DoesNotExist:
            return Response({
                'Status':status.HTTP_404_NOT_FOUND,
                'StatusMsg':"Company data not found",
                'APICode':APICodeClass.User_Edit.value
            },status=status.HTTP_404_NOT_FOUND)
        
        deptId = body_data.get("cmpdeptid") 

        try:
            deptEntry = QitDepartment.objects.get(transid=deptId,cmptransid=cmpId)
        except QitDepartment.DoesNotExist:
            return Response({
                'Status':status.HTTP_404_NOT_FOUND,
                'StatusMsg':"Department data not found",
                'APICode':APICodeClass.User_Edit.value
            },status=status.HTTP_404_NOT_FOUND)
       
        try:
            user = QitUsermaster.objects.get(cmptransid=cmpId, transid=transid)
            # if user.changepassstatus == "0":
            #     request.data.pop("password")
           
            resDB = QitUserlogin.objects.filter(e_mail = user.e_mail).first()
            pwd = request.data.get("password")
            print(pwd)
            if pwd:
                print("here : ",pwd)
                # if not pwd:
                #     return Response({
                #         'Status':400,
                #         'StatusMsg':"password field is required",
                #         'APICode':APICodeClass.User_Edit.value
                #     },status=400)
                user.changepassstatus = 0
                newPassword = make_password(pwd)
                user.password = newPassword
                resDB.password = newPassword
                message1 =  send_credential_email(user.username,user.e_mail,pwd)
                send_html_mail(f"Updated Credentials",message1,[user.e_mail])
            user.cmpdeptid = deptEntry
            user.gender = body_data.get("gender")
            user.phone = body_data.get("phone")
            user.save()
            resDB.save()
            return Response({
                'Status':200,
                'StatusMsg':"User data updated",
                'APICode':APICodeClass.User_Edit.value
            },status=200)
        except QitUsermaster.DoesNotExist:
            return Response({
                'Status':status.HTTP_404_NOT_FOUND,
                'StatusMsg':"User data not found",
                'APICode':APICodeClass.User_Edit.value
            },status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'Status':status.HTTP_404_NOT_FOUND,
            'StatusMsg':str(e),
                'APICode':APICodeClass.User_Edit.value
        },status=status.HTTP_404_NOT_FOUND)

# @api_view(['PUT'])
# def reset_user_password(request,cmpId, transid):
#     try:
#         user = QitUsermaster.objects.get(cmptransid=cmpId, transid=transid)
#     except QitUsermaster.DoesNotExist:
#         return Response({
#                     'Status':status.HTTP_404_NOT_FOUND,
#                     'StatusMsg':"No data found"
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
                    'StatusMsg':"No data found",
                    'APICode':APICodeClass.User_Delete.value  
                },status=status.HTTP_404_NOT_FOUND)
    try:
        userLogin = QitUserlogin.objects.get(e_mail=user.e_mail,userrole=user.usertype)
    except QitUserlogin.DoesNotExist:
        return Response({
                    'Status':status.HTTP_404_NOT_FOUND,
                    'StatusMsg':"No data found",
                    'APICode':APICodeClass.User_Delete.value 
                },status=status.HTTP_404_NOT_FOUND)
    userLogin.delete()
    user.delete()
    return Response({
                    'Status':200,
                    'StatusMsg':"User Data Deleted!!",
                    'APICode':APICodeClass.User_Delete.value 
                })


@api_view(['PUT'])
def update_user_profile(request):
    try:
        body_data = request.data
        if not body_data:
            return Response({'Status': 400, 'StatusMsg': "Payload required",'APICode':APICodeClass.User_Profile_Edit.value}, status=400)        
        cmpId = body_data.get("company_id")
        if not cmpId:
            return Response({'Status': 400, 'StatusMsg': "Company ID required",'APICode':APICodeClass.User_Profile_Edit.value}, status=400)  
        transid = body_data.get("transid")
        if not transid:
            return Response({'Status': 400, 'StatusMsg': "User ID required",'APICode':APICodeClass.User_Profile_Edit.value}, status=400)
   
        try:
            companyEntry = QitCompany.objects.get(transid=cmpId)
        except QitCompany.DoesNotExist:
            return Response({
                'Status':status.HTTP_404_NOT_FOUND,
                'StatusMsg':"Company data not found",
                'APICode':APICodeClass.User_Profile_Edit.value
            },status=status.HTTP_404_NOT_FOUND)
        
        deptId = body_data.get("department_id") 

        try:
            deptEntry = QitDepartment.objects.get(transid=deptId,cmptransid=cmpId)
        except QitDepartment.DoesNotExist:
            return Response({
                'Status':status.HTTP_404_NOT_FOUND,
                'StatusMsg':"Department data not found",
                'APICode':APICodeClass.User_Profile_Edit.value
            },status=status.HTTP_404_NOT_FOUND)
       
        try:
            user = QitUsermaster.objects.get(cmptransid=cmpId, transid=transid)
           
            user.cmpdeptid = deptEntry
            user.gender = body_data.get("gender")
            user.phone = body_data.get("phone")
            user.username = body_data.get("username")
            user.save()
            return Response({
                'Status':200,
                'StatusMsg':"User profile data updated",
                'APICode':APICodeClass.User_Profile_Edit.value
            },status=200)
        except QitUsermaster.DoesNotExist:
            return Response({
                'Status':status.HTTP_404_NOT_FOUND,
                'StatusMsg':"User data not found",
                'APICode':APICodeClass.User_Profile_Edit.value
            },status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'Status':status.HTTP_404_NOT_FOUND,
            'StatusMsg':str(e),
            'APICode':APICodeClass.User_Profile_Edit.value
        },status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_user_by_company(request, cmpId):
    try:
        companyEntry = QitCompany.objects.filter(transid=cmpId).first()
        if not companyEntry:
            return Response({
                'Status': 400,
                'StatusMsg': "Company not found",
                'APICode': APICodeClass.User_Get.value
            }, status=400)

        users = QitUsermaster.objects.filter(cmptransid=cmpId)
        

        serializer = UserShortDataSerializer(users, many=True)  # Set many=True
        return Response({
            'Data': serializer.data,
            'APICode': APICodeClass.User_GetById.value
        })

    except QitUsermaster.DoesNotExist:
        return Response({
            'Status': 404,
            'StatusMsg': 'User not found',
            'APICode': APICodeClass.User_GetById.value
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            'Status': 400,
            'StatusMsg': str(e),
            'APICode': APICodeClass.User_GetById.value
        }, status=400)
    