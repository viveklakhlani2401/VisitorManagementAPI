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
        companies = QitCompany.objects.all()
        serializer = CompanyMasterDetailsGetSerializer(companies, many=True)
        return Response({
            'data':serializer.data,
            'APICode':APICodeClass.Master_Admin_CmpStatus.value
        }, status=status.HTTP_200_OK)
    except QitCompany.DoesNotExist:
        return Response({
            'Status': 400,
            'StatusMsg': "Data not found",
            'APICode':APICodeClass.Master_Admin_CmpStatus.value
        },status=400)  
    except Exception as e:
        return Response({
            'Status': 400,
            'StatusMsg': "Error : " + str(e),
            'APICode':APICodeClass.Master_Admin_CmpStatus.value
        },status=400)  
    
@csrf_exempt
@api_view(["POST"])
def ActiveComapny(request):
    try:
        reqData = request.data
        if reqData["status"] != "I" and reqData["status"] != "A":
            return Response({'Status': 400, 'StatusMsg': "Enter valid status",'APICode':APICodeClass.Master_Admin_CmpStatus.value}, status=400)  
        if reqData["status"] == "I" and reqData["reason"] == "":
            return Response({'Status': 400, 'StatusMsg': "Reason is required",'APICode':APICodeClass.Master_Admin_CmpStatus.value}, status=400) 
        resDB = QitCompany.objects.get(transid = reqData["cmpid"])
        if resDB:
            statusData = ""
            if reqData["status"] == "A":
                statusData = "Activated"
            if reqData["status"] == "I": 
                statusData = "Inactivated"

            if str(resDB.status) == str(reqData["status"]):
                return Response({'Status': 400, 'StatusMsg': f"Company Already {statusData}",'APICode':APICodeClass.Master_Admin_CmpStatus.value}, status=400)      
            
            resDB.status = reqData["status"]
            resDB.reason = reqData["reason"]
            resDB.save()
            return Response({
                'Status':200,
                'StatusMsg':f"Company is {statusData}",
                'APICode':APICodeClass.Master_Admin_CmpStatus.value
            })
        else:
            return Response({
                'Status':400,
                'StatusMsg':"Invalid Company id",
                'APICode':APICodeClass.Master_Admin_CmpStatus.value
            },status=400)
    except QitCompany.DoesNotExist:
        return Response({
            'Status':400,
            'StatusMsg':"No data found",
            'APICode':APICodeClass.Master_Admin_CmpStatus.value
        },status=400)
    except Exception as e:
        return Response({
            'Status':400,
            'StatusMsg':str(e),
            'APICode':APICodeClass.Master_Admin_CmpStatus.value
        },status=400)