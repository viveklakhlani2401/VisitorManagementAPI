from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from QIT.utils.APICode import APICodeClass
from rest_framework import status
from QIT.serializers import CompanyMasterDetailsGetSerializer
from QIT.models import QitCompany

@csrf_exempt
@api_view(['GET'])
def getCmpDetails(request):
    try:
        # cmpEntry = QitCompany.objects.get()
        # print("Company Data : ",cmpEntry)
        # serializer = CompanyMasterGetSerializer(cmpEntry)
        companies = QitCompany.objects.all()
        serializer = CompanyMasterDetailsGetSerializer(companies, many=True)
        return Response({
            'data':serializer.data,
            'APICode':APICodeClass.Config_Get.value
        }, status=status.HTTP_200_OK)
    except QitCompany.DoesNotExist:
        return Response({
            'Status': 400,
            'StatusMsg': "Data not found",
            'APICode':APICodeClass.Config_Get.value
        },status=400)  
    except Exception as e:
        return Response({
            'Status': 400,
            'StatusMsg': "Error : " + str(e),
            'APICode':APICodeClass.Config_Get.value
        },status=400)  