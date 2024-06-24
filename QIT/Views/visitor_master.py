from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from QIT.serializers import QitVisitorinoutPOSTSerializer, QitVisitorSerializer,QitVisitorinoutGETSerializer
from QIT.models import QitVisitormaster,QitVisitorinout,QitCompany
import json
from django.core.cache import cache
from datetime import datetime
from QIT.Views import common
from django.utils import timezone
import pytz
from dateutil import parser

@csrf_exempt
@api_view(['POST'])
def Save_Visitor(request):
    print("hello")
    try:
        print("here")
        body_data = request.data
        print(body_data)
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
        timeslot = body_data.get("timeslot")
        if timeslot:
            try:
                timeslot_datetime = parser.parse(timeslot)
                ist = pytz.timezone('Asia/Kolkata')
                timeslot_datetime_ist = ist.localize(timeslot_datetime)
                timeslot_datetime_utc = timeslot_datetime_ist.astimezone(pytz.utc)
                current_datetime_utc = timezone.now()
                if timeslot_datetime_utc < current_datetime_utc:
                    return Response({
                        'Status': 400,
                        'StatusMsg': "Timeslot cannot be in the past..!!"
                    }, status=400)
            except (ValueError, TypeError) as e:
                return Response({
                    'Status': 400,
                    'StatusMsg': "Invalid timeslot format..!!"
                }, status=400)
        stored_data_json = cache.get(f"otp_{email}")
        if stored_data_json:
            stored_data = json.loads(stored_data_json)
            stored_status = stored_data['status']
            stored_role = stored_data['role']
            if stored_status == 1 and stored_role.upper() == "VISITOR" :
                dataToSerialize = request.data
                companyEntry = QitCompany.objects.filter(transid=dataToSerialize["company_id"]).first()
                print("here")
                if not companyEntry:
                    return Response( {
                        'isSaved':"N",
                        'Status': 400,
                        'StatusMsg': "Company not found..!!"
                    }, status=400)
                dataToSerialize["cmpdepartmentid"]=dataToSerialize["department_id"]
                dataToSerialize["cmptransid"]=dataToSerialize["company_id"]
                dataToSerialize.pop("company_id")
                dataToSerialize.pop("department_id")
                serializer = QitVisitorinoutPOSTSerializer(data=dataToSerialize)
                if serializer.is_valid():
                    visitorinout = serializer.save()
                    print(visitorinout["visitortansid"].e_mail)
                    state = "Pending"
                    if visitorinout['checkinstatus'] == "P" : 
                        state = "Pending"
                    elif visitorinout['checkinstatus'] == "R" : 
                        state = "Rejected"
                    elif visitorinout['checkinstatus'] == "A" : 
                        state = "Approved"
                    visitor_dict = {
                        'id': visitorinout['id'],
                        'vName': visitorinout['visitortansid'].vname,
                        'vPhone1':visitorinout['visitortansid'].phone1,
                        'vCmpname': visitorinout['visitortansid'].vcmpname,
                        'vLocation': visitorinout['visitortansid'].vlocation,
                        'deptId': visitorinout['cmpdepartmentid'].transid,
                        'deptName': visitorinout['cmpdepartmentid'].deptname,
                        'vEmail': visitorinout['visitortansid'].e_mail,
                        'state': state,
                        'status': visitorinout['checkinstatus'],
                        'addedBy': visitorinout['createdby'],
                        'cnctperson': visitorinout['cnctperson'],
                        'timeslot':  visitorinout['timeslot'].isoformat() if visitorinout['timeslot'] else None,
                        'purposeofvisit': visitorinout['purposeofvisit'],
                        'reason': visitorinout['reason']
                    }
                    common.send_visitors(visitor_dict,dataToSerialize["cmptransid"],"add")
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

        companyEntry = QitCompany.objects.filter(transid=cmpid).first()
        if not companyEntry:
            return Response( {
                'Status': 400,
                'StatusMsg': "Company not found..!!"
            }, status=400)

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
        

        companyEntry = QitCompany.objects.filter(transid=cid).first()
        if not companyEntry:
            return Response( {
                'Status': 400,
                'StatusMsg': "Company not found..!!"
            }, status=400)
        if status.upper() == "ALL":
            queryset = QitVisitorinout.objects.filter(cmptransid=cid).order_by('-checkintime', '-entrydate')
        elif status.upper() == "P":
            queryset = QitVisitorinout.objects.filter(cmptransid=cid,status="P").order_by('-checkintime', '-entrydate')
        else:
            return Response({'Status': 400, 'StatusMsg': "Invalid state..!!"}, status=400)
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
        

        companyEntry = QitCompany.objects.filter(transid=cid).first()
        if not companyEntry:
            return Response( {
                'Status': 400,
                'StatusMsg': "Company not found..!!"
            }, status=400)
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
        
        

        companyEntry = QitCompany.objects.filter(transid=reqData["company_id"]).first()
        if not companyEntry:
            return Response( {
                'Status': 400,
                'StatusMsg': "Company not found..!!"
            }, status=400)

        inoutEntry = QitVisitorinout.objects.filter(transid=reqData["visitor_id"],cmptransid=reqData["company_id"]).first()
        if not inoutEntry:
            return Response({'Status': 400, 'StatusMsg': "Data not found..!!"}, status=400)
        if inoutEntry.status.upper() == "A":
            return Response({'Status': 400, 'StatusMsg': "Visitor already approved..!!"}, status=400)
        if inoutEntry.status.upper() == "R":
            return Response({'Status': 400, 'StatusMsg': "Visitor already rejected..!!"}, status=400)
        
        # Timeslot validation
        timeslot = inoutEntry.timeslot
        if timeslot:
            try:
                ist = pytz.timezone('Asia/Kolkata')
                if isinstance(timeslot, str):
                    # If timeslot is a string, parse it
                    timeslot = datetime.strptime(timeslot, "%Y-%m-%d %H:%M:%S")

                if timeslot.tzinfo is None:
                    # If timeslot is naive, localize it to IST
                    timeslot_datetime_ist = ist.localize(timeslot)
                else:
                    # If timeslot is already aware, just ensure it is in IST
                    timeslot_datetime_ist = timeslot.astimezone(ist)

                timeslot_datetime_utc = timeslot_datetime_ist.astimezone(pytz.utc)
                current_datetime_utc = timezone.now()
                
                if current_datetime_utc > timeslot_datetime_utc:
                    if current_datetime_utc.date() != timeslot_datetime_utc.date():
                        return Response({'Status': 400, 'StatusMsg': "Cannot verify. Timeslot is more than one day old..!!"}, status=400)   
                    # return Response({'Status': 400, 'StatusMsg': "Cannot verify. Timeslot is more than one day old..!!"}, status=400)
            except Exception as e:
                return Response({'Status': 400, 'StatusMsg': f"Error processing timeslot: {str(e)}"}, status=400)
        
        inoutEntry.status = reqData["status"].upper()
        inoutEntry.reason = reqData["reason"]
        if state.upper() == "A":
            inoutEntry.checkintime = datetime.now()
        inoutEntry.save()
        common.send_visitors(inoutEntry,reqData["company_id"],"verify")

        return Response({'Status': 200, 'StatusMsg': "Status updated..!!"}, status=200)
    except Exception as e:
        return Response({'Status': 400, 'StatusMsg': str(e)}, status=400)
         


# get visitor status by email
@csrf_exempt
@api_view(["POST"])
def chkStatus(request):
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
            return Response({'Status': 400, 'StatusMsg': "Visitor data not found..!!"}, status=400)
        

        companyEntry = QitCompany.objects.filter(transid=cmpid).first()
        if not companyEntry:
            return Response( {
                'isSaved':"N",
                'Status': 400,
                'StatusMsg': "Company not found..!!"
            }, status=400)
        inOutEntry = QitVisitorinout.objects.filter(visitortansid=visitor_entry.transid).order_by("-entrydate").first()
        if not inOutEntry:
            return Response({'Status': 400, 'StatusMsg': "Visitor request entry not found..!!"}, status=400)

        return Response({
            'e_mail':visitor_entry.e_mail,
            'status':inOutEntry.status
        }, status=200)
        
    except Exception as e:
        return Response({'Status': 400, 'StatusMsg': "An error occurred: {}".format(str(e))}, status=400)
    

# checkout visitor email
@csrf_exempt
@api_view(["POST"])
def checkoutVisitor(request):
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
        
        companyEntry = QitCompany.objects.filter(transid=cmpid).first()
        if not companyEntry:
            return Response( {
                'isSaved':"N",
                'Status': 400,
                'StatusMsg': "Company not found..!!"
            }, status=400)

        visitor_entry = QitVisitormaster.objects.filter(e_mail=email, cmptransid=cmpid).first()
        if not visitor_entry:
            return Response({'Status': 400, 'StatusMsg': "Visitor data not found..!!"}, status=400)

        
        inOutEntry = QitVisitorinout.objects.filter(visitortansid=visitor_entry.transid).order_by("-entrydate").first()
        if not inOutEntry:
            return Response({'Status': 400, 'StatusMsg': "Visitor checkin entry not found..!!"}, status=400)
        
        if inOutEntry.status.upper() != "A":
            return Response({'Status': 400, 'StatusMsg': "Visitor status is not approve..!!"}, status=400)

        
        inOutEntry.checkouttime = datetime.now()
        inOutEntry.checkinstatus = "O"

        inOutEntry.save()

        return Response({'Status': 200, 'StatusMsg': "Checkout successfullyy..!!"}, status=200)
        
    except Exception as e:
        return Response({'Status': 400, 'StatusMsg': "An error occurred: {}".format(str(e))}, status=400)

    