from QIT.models import QitCompanymaster,QitOtp,QitUserlogin
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from QIT.serializers import CompanyMasterSerializer,CompanyMasterGetSerializer
from rest_framework import status
import hashlib
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
load_dotenv()
from .common import create_userlogin
from QIT.serializers import CompanyMasterGetSerializer

# Register Company API
@csrf_exempt
@api_view(["POST"])
def CreateCompany(request):
    body_data = request.data
    try:
        if not body_data["e_mail"]:
            return Response({
                'Status':400,
                'StatusMsg':"Email is required..!!"
            })
        if not body_data["password"]:
            return Response({
                'Status':400,
                'StatusMsg':"Password is required..!!"
            })
        if not body_data["businessname"]:
            return Response({
                'Status':400,
                'StatusMsg':"BusinessName is required..!!"
            })
        if not body_data["businesslocation"]:
            return Response({
                'Status':400,
                'StatusMsg':"BUsinessLocation is required..!!"
            })
        
        OTPEntry = QitOtp.objects.filter(e_mail=body_data["e_mail"]).first()
        if OTPEntry is None:
            return Response({
                'Status': 400,
                'StatusMsg': "Email is not verified..!!."
            })
 
        if OTPEntry.status != 'Y':
            return Response({
                'Status': 400,
                'StatusMsg': "OTP is not verified..!!"
            })
        
        emailExistInComapny = QitCompanymaster.objects.filter(e_mail = body_data["e_mail"])
        if(emailExistInComapny):
            return Response({
                'Status':400,
                'StatusMsg':"This email alredy register as comapny..!!"
            })
        
        OTPEntry = QitOtp.objects.filter(e_mail=body_data["e_mail"]).first()
        if OTPEntry is None:
            return Response({
                'Status': 400,
                'StatusMsg': "No entry found for this email."
            })

        print("OTPEntry Status: " + OTPEntry.status)

        if OTPEntry.status != 'Y':
            return Response({
                'Status': 400,
                'StatusMsg': "This Company is not verified..!!"
            })

        
        serializer = CompanyMasterSerializer(data=request.data)
        if serializer.is_valid():
            company_master = serializer.save()
            company_master.status = "A"
            unique_string = f"{body_data['e_mail']}_{body_data['businessname']}_{body_data['businesslocation']}"
            unique_hash = hashlib.sha256(unique_string.encode('utf-8')).hexdigest()
            company_master.qrcodeid = unique_hash
            company_master.save()
            create_userlogin(body_data["e_mail"],body_data["password"],"COMPANY")
            frontendURL = os.getenv("FRONTEND_URL")
            secret = os.getenv("SECRETE")
            if QitCompanymaster.objects.filter(transid=company_master.transid).exists():
                frontendURL = os.getenv("FRONTEND_URL")
                if frontendURL is None:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                return Response({
                    # 'data': serializer.data,
                    'status': status.HTTP_201_CREATED,
                    'StatusMsg':"Registered successfully..!!",
                    'encodedString': f"{frontendURL}{unique_hash}"
                })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'Status': 400,
            'StatusMsg': "Error : " + str(e)
        })  


@csrf_exempt
@api_view(["GET"])
def GetComapnyData(request):
    # print()
    qrCode = request.query_params.get("qrCode")

    resDB = QitCompanymaster.objects.filter(qrcodeid = qrCode)
    print(resDB)
    serializer = CompanyMasterGetSerializer(resDB,many=True)
    print(serializer.data)
    if resDB:
        return Response(serializer.data)
    else:
        return Response({
            'Status':400,
            'StatusMsg':"Invalid QR Code..!!"
        })

    
# Create User login for ALL type of User
def create_userlogin(useremail, password, userrole):
    userlogin = QitUserlogin(useremail=useremail, password=password, userrole=userrole)
    userlogin.save()
    return userlogin

# All companys data
@csrf_exempt
@api_view(['GET'])
def getCompany(request):
    companies = QitCompanymaster.objects.all()
    serializer = CompanyMasterGetSerializer(companies, many=True)
    return Response(serializer.data)
