from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from QIT.serializers import QitVisitorinoutPOSTSerializer, QitVisitorSerializer,QitVisitorinoutGETSerializer
from QIT.models import QitVisitormaster,QitVisitorinout
import json
from django.core.cache import cache
from datetime import datetime
from QIT.Views import common
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
                serializer = QitVisitorinoutPOSTSerializer(data=dataToSerialize)
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


# for get isitor data on mobile view
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
    
# get all visior data for company
@csrf_exempt
@api_view(["GET"])
def GetAllVisitor(request,status,cid):
    try:
        if not cid:
            return Response({'Status': 400, 'StatusMsg': "Company Id requied..!!"}, status=400)
        # queryset = QitVisitorinout.objects.filter(cmptransid=cid)
        # queryset = QitVisitorinout.objects.filter(cmptransid=cid)
        # entrydate_info = [(type(obj.entrydate), obj.entrydate) for obj in queryset]  # Collect type and value of entrydate field
        
        # print("Entrydate info:", entrydate_info)  # Debug statement

        # queryset = queryset.annotate(
        #     sorting_date=Case(
        #         When(checkintime=False, then=F('checkindatetime')),
        #         default=F('entrydate'),
        #         output_field=models.DateTimeField()
        #     )
        # ).order_by('-sorting_date')
        if status.upper() == "ALL":
            queryset = QitVisitorinout.objects.filter(cmptransid=cid).order_by('-checkintime', '-entrydate')
        elif status.upper() == "P":
            queryset = QitVisitorinout.objects.filter(cmptransid=cid,status="P").order_by('-checkintime', '-entrydate')
        else:
            return Response({'Status': 400, 'StatusMsg': "Invalid state..!!"}, status=400)
        print(queryset)
        if not queryset:
            return Response({'Status': 400, 'StatusMsg': "No data..!!"}, status=400)
        serializer = QitVisitorinoutGETSerializer(queryset, many=True)
        return Response(serializer.data,status=200)
    except Exception as e:
        return Response({'Status': 400, 'StatusMsg': str(e)}, status=400)

# get a visior data for company
@csrf_exempt
@api_view(["GET"])
def GetVisitorDetail(request,vid,cid):
    try:
        if not cid:
            return Response({'Status': 400, 'StatusMsg': "Company Id requied..!!"}, status=400)
        if not vid:
            return Response({'Status': 400, 'StatusMsg': "Visitor Id requied..!!"}, status=400)
        queryset = QitVisitorinout.objects.filter(cmptransid=cid,transid=vid).first()
        if not queryset:
            return Response({'Status': 400, 'StatusMsg': "No data..!!"}, status=400)
        serializer = QitVisitorinoutGETSerializer(queryset, many=False)
        return Response(serializer.data,status=200)
    except Exception as e:
        return Response({'Status': 400, 'StatusMsg': str(e)}, status=400)

# verify pending visitor
@csrf_exempt
@api_view(["POST"])
def verifyVisitor(request):
    try:
        reqData = request.data
        if not reqData:
            return Response({'Status': 400, 'StatusMsg': "Payload required..!!"}, status=400)  
        if not reqData["company_id"]:
            return Response({'Status': 400, 'StatusMsg': "company_id required..!!"}, status=400)
        if not reqData["visitor_id"]:
            return Response({'Status': 400, 'StatusMsg': "visitor_id required..!!"}, status=400)  
        if not reqData["reason"]:
            return Response({'Status': 400, 'StatusMsg': "reason required..!!"}, status=400)  
        if not reqData["status"]:
            return Response({'Status': 400, 'StatusMsg': "status required..!!"}, status=400) 
        state =  reqData["status"]
        if state.upper() != "A" and state.upper() != "R":
            return Response({'Status': 400, 'StatusMsg': "Enter valid status..!!"}, status=400) 

        inoutEntry = QitVisitorinout.objects.filter(transid=reqData["visitor_id"],cmptransid=reqData["company_id"]).first()
        if not inoutEntry:
            return Response({'Status': 400, 'StatusMsg': "Data not found..!!"}, status=400)
        inoutEntry.status = reqData["status"].upper()
        inoutEntry.reason = reqData["reason"]
        if state.upper() == "A":
            inoutEntry.checkintime = datetime.now()
        inoutEntry.save()
        print("inoutEntry : ",inoutEntry)
        common.send_visitors(inoutEntry,reqData["company_id"])
        return Response({'Status': 200, 'StatusMsg': "Status updated..!!"}, status=200)
    except Exception as e:
        return Response({'Status': 400, 'StatusMsg': str(e)}, status=400)
         