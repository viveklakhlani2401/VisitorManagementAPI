from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from QIT.serializers import QitVisitorinoutSerializer, QitVisitorSerializer
from QIT.models import QitVisitormaster
import json
from django.core.cache import cache

@csrf_exempt
@api_view(['POST'])
def Save_Visitor(request):
    try:
        body_data = request.data
        
        # print(dataToSerialize)
        if not body_data:
            return Response({
                'Status': 400,
                'StatusMsg': "Payload required..!!"
            },status=400)  
        email = body_data["e_mail"]
        if not email:
            return Response({
                'Status': 400,
                'StatusMsg': "e_mail is required..!!"
            },status=400)  
        if not body_data["company_id"]:
            return Response({
                'Status': 400,
                'StatusMsg': "cmptransid is required..!!"
            },status=400)  
        stored_data_json = cache.get(f"otp_{email}")
        if stored_data_json:
            stored_data = json.loads(stored_data_json)
            stored_status = stored_data['status']
            stored_role = stored_data['role']
            if stored_status == 1 and stored_role.upper() == "VISITOR" :
                dataToSerialize = request.data
                dataToSerialize = request.data
                dataToSerialize["cmpdepartmentid"]=dataToSerialize["department_id"]
                dataToSerialize["cmptransid"]=dataToSerialize["company_id"]
                dataToSerialize.pop("company_id")
                dataToSerialize.pop("department_id")
                serializer = QitVisitorinoutSerializer(data=dataToSerialize)
                if serializer.is_valid():
                    serializer.save()
                    return Response( {
                        'isSaved':"Y",
                        'Status': 201,
                        'StatusMsg': "Visitor saved..!!"
                    }, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'Status': 400,
                    'StatusMsg': "OTP is not verified..!!"
                },status=400)
        else:
            return Response({
                'Status': 400,
                'StatusMsg': "Email not found or OTP expired..!!"
            },status=400)  
    except Exception as e:
        return Response({
            'Status':400,
            'StatusMsg':str(e)
        },status=400)


# @csrf_exempt
# @api_view(['POST'])
# def GetVisitorByE_Mail(request):
#     try:
#         body_data = request.data
#         if not body_data:
#             return Response({
#                 'Status': 400,
#                 'StatusMsg': "Payload required..!!"
#             },status=400)  
#         if not body_data["e_mail"]:
#             return Response({
#                 'Status': 400,
#                 'StatusMsg': "e_mail is required..!!"
#             },status=400)  
#         if not body_data["company_id"]:
#             return Response({
#                 'Status': 400,
#                 'StatusMsg': "cmptransid is required..!!"
#             },status=400)  
#         email = body_data["e_mail"]
#         cmpid = body_data["company_id"]
#         visitorEntry = QitVisitormaster.objects.filter(e_mail=email,cmptransid=cmpid).first()
#         if not visitorEntry:
#             return Response({
#                 'Status':400,
#                 'StatusMsg':"No data found..!!"
#             },status=400)
#         serializedData = QitVisitorSerializer(data=visitorEntry)
#         if serializedData.is_valid():
#             return Response({serializedData.data},status=200)
#         else:
#             return Response(serializedData.error_messages,status=400)
            
#     except Exception as e:
#         return Response({
#             'Status':400,
#             'StatusMsg':str(e)
#         },status=400)



@csrf_exempt
@api_view(['POST'])
def GetVisitorByE_Mail(request):
    try:
        body_data = request.data
        if not body_data:
            return Response({'Status': 400, 'StatusMsg': "Payload required..!!"}, status=400)  
        
        email = body_data.get("e_mail")
        cmpid = body_data.get("company_id")
        
        if not email:
            return Response({'Status': 400, 'StatusMsg': "Email is required..!!"}, status=400)  
        if not cmpid:
            return Response({'Status': 400, 'StatusMsg': "Company ID is required..!!"}, status=400)  

        visitor_entry = QitVisitormaster.objects.filter(e_mail=email, cmptransid=cmpid).first()
        if not visitor_entry:
            return Response({'Status': 400, 'StatusMsg': "No data found..!!"}, status=400)

        serialized_data = QitVisitorSerializer(visitor_entry)
        return Response(serialized_data.data, status=200)
        
    except Exception as e:
        return Response({'Status': 400, 'StatusMsg': "An error occurred: {}".format(str(e))}, status=400)