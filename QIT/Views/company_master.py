from QIT.models import QitCompany,QitOtp
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from QIT.serializers import CompanyMasterSerializer,CompanyMasterGetSerializer, CompanyProfileSerializer
from rest_framework import status
import hashlib
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
load_dotenv()
from .common import create_userlogin,create_comp_auth,create_comp_notification_auth
from QIT.serializers import CompanyMasterGetSerializer
from django.core.cache import cache
import json
from QIT.utils.APICode import APICodeClass
from QIT.models import QitDepartment

# Register Company API
@csrf_exempt
@api_view(["POST"])
def CreateCompany(request):
    body_data = request.data
    try:
        if not body_data["e_mail"]:
            return Response({
                'Status':400,
                'StatusMsg':"Email is required..!!",
                'APICode':APICodeClass.Company_Save.value
            },status=400)
        if not body_data["password"]:
            return Response({
                'Status':400,
                'StatusMsg':"Password is required..!!",
                'APICode':APICodeClass.Company_Save.value
            },status=400)
        if not body_data["bname"]:
            return Response({
                'Status':400,
                'StatusMsg':"BusinessName is required..!!",
                'APICode':APICodeClass.Company_Save.value
            },status=400)
        if not body_data["blocation"]:
            return Response({
                'Status':400,
                'StatusMsg':"BUsinessLocation is required..!!",
                'APICode':APICodeClass.Company_Save.value
            },status=400)
        
        # OTPEntry = QitOtp.objects.filter(e_mail=body_data["e_mail"]).first()
        # if OTPEntry is None:
        #     return Response({
        #         'Status': 400,
        #         'StatusMsg': "Email is not verified..!!."
        #     })
 
        # if OTPEntry.status != 'Y':
        #     return Response({
        #         'Status': 400,
        #         'StatusMsg': "OTP is not verified..!!"
        #     })
        
        emailExistInComapny = QitCompany.objects.filter(e_mail = body_data["e_mail"])
        if(emailExistInComapny):
            return Response({
                'Status':400,
                'StatusMsg':"This email alredy register as comapny..!!",
                'APICode':APICodeClass.Company_Save.value
            },status=400)
        
        # OTPEntry = QitOtp.objects.filter(e_mail=body_data["e_mail"]).first()
        # if OTPEntry is None:
        #     return Response({
        #         'Status': 400,
        #         'StatusMsg': "No entry found for this email."
        #     })


        # if OTPEntry.status != 'Y':
        #     return Response({
        #         'Status': 400,
        #         'StatusMsg': "This Company is not verified..!!"
        #     })
        stored_data_json = cache.get(f"otp_{body_data['e_mail']}")
        if stored_data_json:
            stored_data = json.loads(stored_data_json)
            stored_status = stored_data['status']
            stored_role = stored_data['role']
            if stored_status == 1 and stored_role.upper() == "COMPANY" :
                serializer = CompanyMasterSerializer(data=request.data)
                if serializer.is_valid():
                    company_master = serializer.save()
                    company_master.status = "A"
                    unique_string = f"{body_data['e_mail']}_{body_data['bname']}_{body_data['blocation']}"
                    unique_hash = hashlib.sha256(unique_string.encode('utf-8')).hexdigest()
                    company_master.qrstring = unique_hash
                    company_master.save()
                    QitDepartment.objects.create(deptname="Default", cmptransid=company_master)
                    create_userlogin(body_data["e_mail"],body_data["password"],"COMPANY")
                    create_comp_auth(company_master.transid,company_master,"COMPANY")
                    create_comp_notification_auth(company_master.transid,company_master,"COMPANY")
                    frontendURL = os.getenv("FRONTEND_URL")
                    if QitCompany.objects.filter(transid=company_master.transid).exists():
                        frontendURL = os.getenv("FRONTEND_URL")
                        if frontendURL is None:
                            return Response({
                                'error':serializer.errors,
                                'APICode':APICodeClass.Company_Save.value
                            }, status=status.HTTP_400_BAD_REQUEST)
                        return Response({
                            # 'data': serializer.data,
                            'status': status.HTTP_201_CREATED,
                            'StatusMsg':"Registered successfully..!!",
                            'encodedString': unique_hash,
                            'APICode':APICodeClass.Company_Save.value
                        })
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {
                    'Status': 400,
                    'StatusMsg': "OTP is not verified..!!",
                    'APICode':APICodeClass.Company_Save.value
                }
                return Response(response,status=400)
        else:
            response = {
                    'Status': 400,
                    'StatusMsg': "Email not found or OTP expired..!!",
                    'APICode':APICodeClass.Company_Save.value
                }
            return Response(response,status=400)
    except Exception as e:
        return Response({
            'Status': 400,
            'StatusMsg': "Error : " + str(e),
            'APICode':APICodeClass.Company_Save.value
        },status=400)  


@csrf_exempt
@api_view(["GET"])
def GetComapnyData(request,qrCode):
    try:
        resDB = QitCompany.objects.filter(qrstring = qrCode)
        serializer = CompanyMasterGetSerializer(resDB,many=True)
        if resDB:
            return Response({
                'Data':serializer.data,
                'APICode':APICodeClass.Company_GetByQR.value
            })
        else:
            return Response({
                'Status':400,
                'StatusMsg':"Invalid QR Code..!!",
                'APICode':APICodeClass.Company_GetByQR.value
            },status=400)
    except Exception as e:
        return Response({
            'Status':400,
            'StatusMsg':str(e),
            'APICode':APICodeClass.Company_GetByQR.value
        },status=400)



    

@csrf_exempt
@api_view(["GET"])
def GetComapnyDataById(request,cid):
    try:
        resDB = QitCompany.objects.get(transid = cid)
        serializer = CompanyProfileSerializer(resDB,many=False)
        if resDB:
            return Response({
                'Data':serializer.data,
                'APICode':APICodeClass.Company_GetByCId.value
            })
        else:
            return Response({
                'Status':400,
                'StatusMsg':"Invalid Company id..!!",
                'APICode':APICodeClass.Company_GetByCId.value
            },status=400)
    except QitCompany.DoesNotExist:
        return Response({
            'Status':400,
            'StatusMsg':"No data found..!!",
            'APICode':APICodeClass.Company_GetByCId.value
        },status=400)
    except Exception as e:
        return Response({
            'Status':400,
            'StatusMsg':str(e),
            'APICode':APICodeClass.Company_GetByCId.value
        },status=400)



# All companys data
@csrf_exempt
@api_view(['GET'])
def getCompany(request):
    companies = QitCompany.objects.all()
    serializer = CompanyMasterGetSerializer(companies, many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(["PUT"])
def EditComapnyDataById(request):
    try:
        reqData = request.data
        resDB = QitCompany.objects.get(transid = reqData["transid"])
        if resDB:
            resDB.bname = reqData["bname"]
            resDB.blocation = reqData["blocation"]
            resDB.zipcode = reqData["zipcode"]
            resDB.city = reqData["city"]
            resDB.state = reqData["state"]
            resDB.country = reqData["country"]
            resDB.phone1 = reqData["phone1"]
            resDB.phone2 = reqData["phone2"]
            resDB.websitelink = reqData["websitelink"]
            resDB.cmplogo = reqData["cmplogo"]
            resDB.save()
            return Response({
                'Status':200,
                'StatusMsg':"Company data updated..!!",
                'APICode':APICodeClass.Company_Edit.value
            })
        else:
            return Response({
                'Status':400,
                'StatusMsg':"Invalid Company id..!!",
                'APICode':APICodeClass.Company_Edit.value
            },status=400)
    except QitCompany.DoesNotExist:
        return Response({
            'Status':400,
            'StatusMsg':"No data found..!!",
            'APICode':APICodeClass.Company_Edit.value
        },status=400)
    except Exception as e:
        return Response({
            'Status':400,
            'StatusMsg':str(e),
            'APICode':APICodeClass.Company_Edit.value
        },status=400)
