from QIT.models import QitCompanymaster
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from QIT.serializers import CompanyMasterSerializer
from rest_framework import status
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
        
        emailExistInComapny = QitCompanymaster.objects.filter(e_mail = body_data["e_mail"])
        if(emailExistInComapny):
            return Response({
                'Status':400,
                'StatusMsg':"This email alredy register as comapny..!!"
            })
        
        serializer = CompanyMasterSerializer(data=request.data)
        if serializer.is_valid():
            company_master = QitCompanymaster(**serializer.validated_data)
            company_master.status = "A"
            company_master.qrcodeid = "hgfvgh"
            company_master.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'Status': 400,
            'StatusMsg': "Error : " + str(e)
        })  