from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from QIT.serializers import QitVisitorinoutPOSTSerializer, QitVisitorSerializer,QitVisitorinoutGETSerializer
from QIT.models import QitVisitormaster,QitVisitorinout,QitCompany,QitDepartment,QitUsermaster,QitConfigmaster
import json,os
from django.core.cache import cache
from datetime import datetime
from QIT.Views import common
from django.utils import timezone
import pytz
from dateutil import parser
from QIT.utils.APICode import APICodeClass
from django.db.models import DateField
from django.db.models.functions import Cast
from django.utils.timezone import make_aware,now
from .template import send_reminder
from .send_email import send_html_mail

@csrf_exempt
@api_view(['POST'])
def Save_Visitor(request):
    try:
        body_data = request.data
        if not body_data:
            return Response({
                'Status': 400,
                'StatusMsg': "Payload required",
                'APICode':APICodeClass.Visitor_Save.value
            },status=400)  
        email = body_data["e_mail"]
        if not email:
            return Response({
                'Status': 400,
                'StatusMsg': "e_mail is required",
                'APICode':APICodeClass.Visitor_Save.value
            },status=400)  
        if not body_data["company_id"]:
            return Response({
                'Status': 400,
                'StatusMsg': "cmptransid is required",
                'APICode':APICodeClass.Visitor_Save.value
            },status=400)  
       
        alredyEmailChk = QitVisitormaster.objects.filter(e_mail=body_data["e_mail"]).first()

        if alredyEmailChk:
       
            # Get today's date
            today = datetime.now().date()
 
            # Make it timezone aware if necessary (depending on your settings)
            today_start = make_aware(datetime.combine(today, datetime.min.time()))
            today_end = make_aware(datetime.combine(today, datetime.max.time()))
   
            alreadyEntry = QitVisitorinout.objects.filter(visitortansid=alredyEmailChk,entrydate__range=(today_start, today_end),status="P").order_by("-entrydate")
 
            if alreadyEntry:
                return Response({
                    'Status': 400,
                    'StatusMsg': "Visitor request already pending",
                    'APICode':APICodeClass.Visitor_Save.value
                }, status=400)
            
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
                        'StatusMsg': "Timeslot cannot be in the past",
                        'APICode':APICodeClass.Visitor_Save.value
                    }, status=400)
                one_day_ahead = current_datetime_utc + timezone.timedelta(days=1)
                if not body_data.get("createdby") and timeslot_datetime_utc >= one_day_ahead:
                    return Response({
                        'Status': 400,
                        'StatusMsg': "Timeslot cannot be more than one day in the future",
                        'APICode':APICodeClass.Visitor_Save.value
                    }, status=400)
            except (ValueError, TypeError) as e:
                return Response({
                    'Status': 400,
                    'StatusMsg': "Invalid timeslot format",
                    'APICode':APICodeClass.Visitor_Save.value      
                }, status=400)
        stored_data_json = cache.get(f"otp_{email}")
        dataToSerialize = request.data
        ConfiEntry = QitConfigmaster.objects.get(cmptransid=dataToSerialize['company_id'])
        print(ConfiEntry.manualverification)
        if not dataToSerialize["createdby"] or ConfiEntry.manualverification == "Y":
            if stored_data_json:
                stored_data = json.loads(stored_data_json)
                stored_status = stored_data['status']
                stored_role = stored_data['role']
                if stored_status is not 1 and stored_role.upper() is not "VISITOR" :
                    return Response({
                        'Status': 400,
                        'StatusMsg': "OTP is not verified",
                        'APICode':APICodeClass.Visitor_Save.value
                    },status=400)
            else:
                return Response({
                    'Status': 400,
                    'StatusMsg': "Email not found or OTP expired",
                    'APICode':APICodeClass.Visitor_Save.value
                },status=400)  
           
        companyEntry = QitCompany.objects.filter(transid=dataToSerialize["company_id"]).first()
        if not companyEntry:
            return Response( {
                'isSaved':"N",
                'Status': 400,
                'StatusMsg': "Company not found",
                'APICode':APICodeClass.Visitor_Save.value
            }, status=400)
        deptEntry = QitDepartment.objects.filter(transid=dataToSerialize["department_id"]).first()
        if not deptEntry:
            return Response( {
                'isSaved':"N",
                'Status': 400,
                'StatusMsg': "Department not found",
                'APICode':APICodeClass.Visitor_Save.value
            }, status=400)
        dataToSerialize["cmpdepartmentid"]=dataToSerialize["department_id"]
        dataToSerialize["cmptransid"]=dataToSerialize["company_id"]
        dataToSerialize.pop("company_id")
        dataToSerialize.pop("department_id")
        serializer = QitVisitorinoutPOSTSerializer(data=dataToSerialize)
        if serializer.is_valid():
            visitorinout = serializer.save()
            print("visitorinout : ",visitorinout)
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
                'reason': visitorinout['reason'],
                'sortDate':timezone.now().isoformat()
            }
            common.send_visitors(visitor_dict,dataToSerialize["cmptransid"],"add")
            send_email_notification_email(visitor_dict,visitorinout['cmpdepartmentid'],companyEntry.transid)
            return Response( {
                'isSaved':"Y",
                'Status': 201,
                'StatusMsg': "Visitor saved",
                'APICode':APICodeClass.Visitor_Save.value
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except QitConfigmaster.DoesNotExist:
        return Response( {
            'isSaved':"N",
            'Status': 400,
            'StatusMsg': "Company configuration data not found",
            'APICode':APICodeClass.Visitor_Save.value
        }, status=400)
    except Exception as e:
        return Response({
            'Status':400,
            'StatusMsg':str(e),
            'APICode':APICodeClass.Visitor_Save.value
        },status=400)

# @csrf_exempt
# @api_view(['POST'])
# def GetVisitorByE_Mail(request):
#     try:
#         body_data = request.data
#         if not body_data:
#             return Response({
#                 'Status': 400,
#                 'StatusMsg': "Payload required"
#             },status=400)  
#         if not body_data["e_mail"]:
#             return Response({
#                 'Status': 400,
#                 'StatusMsg': "e_mail is required"
#             },status=400)  
#         if not body_data["company_id"]:
#             return Response({
#                 'Status': 400,
#                 'StatusMsg': "cmptransid is required"
#             },status=400)  
#         email = body_data["e_mail"]
#         cmpid = body_data["company_id"]
#         visitorEntry = QitVisitormaster.objects.filter(e_mail=email,cmptransid=cmpid).first()
#         if not visitorEntry:
#             return Response({
#                 'Status':400,
#                 'StatusMsg':"No data found"
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
            return Response({'Status': 400, 'StatusMsg': "Payload required",'APICode':APICodeClass.Visitor_Mobile_GetByEmail.value}, status=400)  
        
        email = body_data.get("e_mail")
        cmpid = body_data.get("company_id")
        
        if not email:
            return Response({'Status': 400, 'StatusMsg': "Email is required",'APICode':APICodeClass.Visitor_Mobile_GetByEmail.value}, status=400)  
        if not cmpid:
            return Response({'Status': 400, 'StatusMsg': "Company ID is required",'APICode':APICodeClass.Visitor_Mobile_GetByEmail.value}, status=400)  

        companyEntry = QitCompany.objects.filter(transid=cmpid).first()
        if not companyEntry:
            return Response( {
                'Status': 400,
                'StatusMsg': "Company not found",
                'APICode':APICodeClass.Visitor_Mobile_GetByEmail.value
            }, status=400)

        visitor_entry = QitVisitormaster.objects.filter(e_mail=email, cmptransid=cmpid).first()
        if not visitor_entry:
            return Response({'Status': 400, 'StatusMsg': "No data found",'APICode':APICodeClass.Visitor_Mobile_GetByEmail.value}, status=400)

        serialized_data = QitVisitorSerializer(visitor_entry)
        return Response(serialized_data.data, status=200)
        
    except Exception as e:
        return Response({'Status': 400, 'StatusMsg': "An error occurred: {}".format(str(e)),'APICode':APICodeClass.Visitor_Mobile_GetByEmail.value}, status=400)
    
# get all visior data for company
@csrf_exempt
@api_view(["GET"])
def GetAllVisitor(request,status,cid):
    try:
        if not cid:
            return Response({'Status': 400, 'StatusMsg': "Company Id requied",'APICode':APICodeClass.Visitor_Get.value}, status=400)
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
                'StatusMsg': "Company not found",
                'APICode':APICodeClass.Visitor_Get.value
            }, status=400)
        if status.upper() == "ALL":
            queryset = QitVisitorinout.objects.filter(cmptransid=cid).order_by('-entrydate','-checkintime')
        elif status.upper() == "P":
            today = timezone.now().date()
            # queryset = QitVisitorinout.objects.filter(cmptransid=cid,status="P").order_by('-checkintime', '-entrydate')
            queryset = QitVisitorinout.objects.annotate(entrydate_date=Cast('entrydate', DateField())).filter(cmptransid=cid, status="P", entrydate_date=today).order_by('-checkintime', '-entrydate')
        
            # queryset = QitVisitorinout.objects.filter(cmptransid=cid,status="P",checkintime=today).order_by('-checkintime', '-entrydate')
        else:
            return Response({'Status': 400, 'StatusMsg': "Invalid state",'APICode':APICodeClass.Visitor_Get.value}, status=400)
        if not queryset:
            return Response({'Status': 400, 'StatusMsg': "No data",'APICode':APICodeClass.Visitor_Get.value}, status=400)
        serializer = QitVisitorinoutGETSerializer(queryset, many=True)
        return Response({'Data':serializer.data,'APICode':APICodeClass.Visitor_Get.value},status=200)
    except Exception as e:
        return Response({'Status': 400, 'StatusMsg': str(e),'APICode':APICodeClass.Visitor_Get.value}, status=400)
 
# get a visior data for company
@csrf_exempt
@api_view(["GET"])
def GetVisitorDetail(request,vid,cid):
    try:
        if not cid:
            return Response({'Status': 400, 'StatusMsg': "Company Id requied",'APICode':APICodeClass.Visitor_GetById.value}, status=400)
        if not vid:
            return Response({'Status': 400, 'StatusMsg': "Visitor Id requied",'APICode':APICodeClass.Visitor_GetById.value}, status=400)
        

        companyEntry = QitCompany.objects.filter(transid=cid).first()
        if not companyEntry:
            return Response( {
                'Status': 400,
                'StatusMsg': "Company not found",
                'APICode':APICodeClass.Visitor_GetById.value
            }, status=400)
        queryset = QitVisitorinout.objects.filter(cmptransid=cid,transid=vid).first()
        if not queryset:
            return Response({'Status': 400, 'StatusMsg': "No data",'APICode':APICodeClass.Visitor_GetById.value}, status=400)
        serializer = QitVisitorinoutGETSerializer(queryset, many=False)
        return Response({'Data':serializer.data,'APICode':APICodeClass.Visitor_GetById.value},status=200)
    except Exception as e:
        return Response({'Status': 400, 'StatusMsg': str(e),'APICode':APICodeClass.Visitor_GetById.value}, status=400)

# verify pending visitor
@csrf_exempt
@api_view(["POST"])
def verifyVisitor(request):
    try:
        reqData = request.data
        if not reqData:
            return Response({'Status': 400, 'StatusMsg': "Payload required",'APICode':APICodeClass.Visitor_Verify.value}, status=400)  
        if not reqData["company_id"]:
            return Response({'Status': 400, 'StatusMsg': "company_id required",'APICode':APICodeClass.Visitor_Verify.value}, status=400)
        if not reqData["visitor_id"]:
            return Response({'Status': 400, 'StatusMsg': "visitor_id required",'APICode':APICodeClass.Visitor_Verify.value}, status=400)
        if not reqData["status"]:
            return Response({'Status': 400, 'StatusMsg': "status required",'APICode':APICodeClass.Visitor_Verify.value}, status=400) 
        state =  reqData["status"]
        if state.upper() != "A" and state.upper() != "R":
            return Response({'Status': 400, 'StatusMsg': "Enter valid status",'APICode':APICodeClass.Visitor_Verify.value}, status=400)   
        if state.upper() == "R":
            if not reqData["reason"]:
                return Response({'Status': 400, 'StatusMsg': "reason required",'APICode':APICodeClass.Visitor_Verify.value}, status=400)  

        companyEntry = QitCompany.objects.filter(transid=reqData["company_id"]).first()
        if not companyEntry:
            return Response( {
                'Status': 400,
                'StatusMsg': "Company not found",
                'APICode':APICodeClass.Visitor_Verify.value
            }, status=400)

        inoutEntry = QitVisitorinout.objects.filter(transid=reqData["visitor_id"],cmptransid=reqData["company_id"]).first()
        if not inoutEntry:
            return Response({'Status': 400, 'StatusMsg': "Data not found",'APICode':APICodeClass.Visitor_Verify.value}, status=400)
        if inoutEntry.status.upper() == "A":
            return Response({'Status': 400, 'StatusMsg': "Visitor already approved",'APICode':APICodeClass.Visitor_Verify.value}, status=400)
        if inoutEntry.status.upper() == "R":
            return Response({'Status': 400, 'StatusMsg': "Visitor already rejected",'APICode':APICodeClass.Visitor_Verify.value}, status=400)
        
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
                        return Response({'Status': 400, 'StatusMsg': "Cannot verify. Timeslot is more than one day old",'APICode':APICodeClass.Visitor_Verify.value}, status=400)   
                    # return Response({'Status': 400, 'StatusMsg': "Cannot verify. Timeslot is more than one day old"}, status=400)
            except Exception as e:
                return Response({'Status': 400, 'StatusMsg': f"Error processing timeslot: {str(e)}",'APICode':APICodeClass.Visitor_Verify.value}, status=400)
        
        inoutEntry.status = reqData["status"].upper()
        inoutEntry.reason = reqData["reason"]
        if state.upper() == "A":
            inoutEntry.checkintime = datetime.now()
            if inoutEntry.createdby == None:
                inoutEntry.checkinstatus = "I"
        inoutEntry.save()
        common.send_visitors(inoutEntry,reqData["company_id"],"verify")

        return Response({'Status': 200, 'StatusMsg': "Status updated",'APICode':APICodeClass.Visitor_Verify.value}, status=200)
    except Exception as e:
        return Response({'Status': 400, 'StatusMsg': str(e),'APICode':APICodeClass.Visitor_Verify.value}, status=400)
         
# get visitor status by email
@csrf_exempt
@api_view(["POST"])
def chkStatus(request):
    try:
        body_data = request.data
        if not body_data:
            return Response({'Status': 400, 'StatusMsg': "Payload required",'APICode':APICodeClass.Visitor_Mobile_ChkStatus.value}, status=400)  
        
        email = body_data.get("e_mail")
        cmpid = body_data.get("company_id")
        
        if not email:
            return Response({'Status': 400, 'StatusMsg': "Email is required",'APICode':APICodeClass.Visitor_Mobile_ChkStatus.value}, status=400)  
        if not cmpid:
            return Response({'Status': 400, 'StatusMsg': "Company ID is required",'APICode':APICodeClass.Visitor_Mobile_ChkStatus.value}, status=400)  
        
        companyEntry = QitCompany.objects.filter(transid=cmpid).first()
        if not companyEntry:
            return Response( {
                'isSaved':"N",
                'Status': 400,
                'StatusMsg': "Company not found",
                'APICode':APICodeClass.Visitor_Mobile_ChkStatus.value
            }, status=400)

        visitor_entry = QitVisitormaster.objects.filter(e_mail=email, cmptransid=cmpid).first()
        if not visitor_entry:
            return Response({'Status': 400, 'StatusMsg': "Visitor data not found",'APICode':APICodeClass.Visitor_Mobile_ChkStatus.value}, status=400)
        
        inOutEntry = QitVisitorinout.objects.filter(visitortansid=visitor_entry.transid).order_by("-entrydate").first()
        if not inOutEntry:
            return Response({'Status': 400, 'StatusMsg': "Visitor request entry not found",'APICode':APICodeClass.Visitor_Mobile_ChkStatus.value}, status=400)
        
        if inOutEntry.checkinstatus:
            return Response({
                'e_mail':visitor_entry.e_mail,
                'status':inOutEntry.checkinstatus,
                'APICode':APICodeClass.Visitor_Mobile_ChkStatus.value
            }, status=200)

        return Response({
            'e_mail':visitor_entry.e_mail,
            'status':inOutEntry.status,
            'APICode':APICodeClass.Visitor_Mobile_ChkStatus.value
        }, status=200)
        
    except Exception as e:
        return Response({'Status': 400, 'StatusMsg': "An error occurred: {}".format(str(e)),'APICode':APICodeClass.Visitor_Mobile_ChkStatus.value}, status=400)
    
# checkout visitor email
@csrf_exempt
@api_view(["POST"])
def checkoutVisitor(request):
    try:
        body_data = request.data
        if not body_data:
            return Response({'Status': 400, 'StatusMsg': "Payload required",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)  
        
        email = body_data.get("e_mail")
        cmpid = body_data.get("company_id")
        
        if not email:
            return Response({'Status': 400, 'StatusMsg': "Email is required",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)  
        if not cmpid:
            return Response({'Status': 400, 'StatusMsg': "Company ID is required",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)  
        
        companyEntry = QitCompany.objects.filter(transid=cmpid).first()
        if not companyEntry:
            return Response( {
                'isSaved':"N",
                'Status': 400,
                'StatusMsg': "Company not found",
                'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value
            }, status=400)

        visitor_entry = QitVisitormaster.objects.filter(e_mail=email, cmptransid=cmpid).first()
        if not visitor_entry:
            return Response({'Status': 400, 'StatusMsg': "Visitor data not found",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)

        
        inOutEntry = QitVisitorinout.objects.filter(visitortansid=visitor_entry.transid).order_by("-entrydate").first()
        if not inOutEntry:
            return Response({'Status': 400, 'StatusMsg': "Visitor checkin entry not found",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)
        
        if inOutEntry.status.upper() != "A":
            return Response({'Status': 400, 'StatusMsg': "Visitor status is not approve",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)
        
        if inOutEntry.checkinstatus.upper() == "O":
            return Response({'Status': 400, 'StatusMsg': "Visitor already checked out",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)


        
        inOutEntry.checkouttime = datetime.now()
        inOutEntry.checkinstatus = "O"

        inOutEntry.save()

        return Response({'Status': 200, 'StatusMsg': "Checkout successfullyy",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=200)
        
    except Exception as e:
        return Response({'Status': 400, 'StatusMsg': "An error occurred: {}".format(str(e)),'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)

# Edit visitor detail
@csrf_exempt
@api_view(["PUT"])
def EditVerifyVisitor(request):
    try:
        body_data = request.data
        if not body_data:
            return Response({'Status': 400, 'StatusMsg': "Payload required",'APICode':APICodeClass.Visitor_Edit.value}, status=400)

        vid = body_data.get("visitor_id")
        cmpid = body_data.get("company_id")
        did = body_data.get("department_id")

        vname = body_data.get("vname")
        # phone1 = body_data.get("phone1", visitor_entry.phone1)
        vcmpname = body_data.get("vcmpname")
        vlocation = body_data.get("vlocation")

        cnctperson = body_data.get("cnctperson")
        purposeofvisit = body_data.get("purposeofvisit")
        anyhardware = body_data.get("anyhardware")

        if not vid:
            return Response({'Status': 400, 'StatusMsg': "Visitor ID is required",'APICode':APICodeClass.Visitor_Edit.value}, status=400)
        if not cmpid:
            return Response({'Status': 400, 'StatusMsg': "Company ID is required",'APICode':APICodeClass.Visitor_Edit.value}, status=400)
        if not did:
            return Response({'Status': 400, 'StatusMsg': "Department ID is required",'APICode':APICodeClass.Visitor_Edit.value}, status=400)
        if not vname:
            return Response({'Status': 400, 'StatusMsg': "Vendor name is required",'APICode':APICodeClass.Visitor_Edit.value}, status=400)
        if not vcmpname:
            return Response({'Status': 400, 'StatusMsg': "Company name is required",'APICode':APICodeClass.Visitor_Edit.value}, status=400)
        if not vlocation:
            return Response({'Status': 400, 'StatusMsg': "Company Location is required",'APICode':APICodeClass.Visitor_Edit.value}, status=400)
        if not cnctperson:
            return Response({'Status': 400, 'StatusMsg': "Contact person name is required",'APICode':APICodeClass.Visitor_Edit.value}, status=400)
        if not purposeofvisit:
            return Response({'Status': 400, 'StatusMsg': "Purpose of Visit is required",'APICode':APICodeClass.Visitor_Edit.value}, status=400)
        
        
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
                        'StatusMsg': "Timeslot cannot be in the past",
                        'APICode':APICodeClass.Visitor_Edit.value
                    }, status=400)
                one_day_ahead = current_datetime_utc + timezone.timedelta(days=1)
                if timeslot_datetime_utc >= one_day_ahead:
                    return Response({
                        'Status': 400,
                        'StatusMsg': "Timeslot cannot be more than one day in the future",
                        'APICode':APICodeClass.Visitor_Edit.value
                    }, status=400)
            except (ValueError, TypeError) as e:
                return Response({
                    'Status': 400,
                    'StatusMsg': "Invalid timeslot format",
                    'APICode':APICodeClass.Visitor_Edit.value
                }, status=400)

        companyEntry = QitCompany.objects.filter(transid=cmpid).first()
        if not companyEntry:
            return Response({'isSaved': "N", 'Status': 400, 'StatusMsg': "Company not found",'APICode':APICodeClass.Visitor_Edit.value}, status=400)

        visitorInOut_entry = QitVisitorinout.objects.filter(transid=vid, cmptransid=cmpid).first()
        if not visitorInOut_entry:
            return Response({'Status': 400, 'StatusMsg': "Visitor data not found",'APICode':APICodeClass.Visitor_Edit.value}, status=400)

        if not visitorInOut_entry.createdby:
            return Response({'Status': 400, 'StatusMsg': "Visitor entry done by external",'APICode':APICodeClass.Visitor_Edit.value}, status=400)
        
        if visitorInOut_entry.status.upper() == "A":
            return Response({'Status': 400, 'StatusMsg': "Visitor status is approved",'APICode':APICodeClass.Visitor_Edit.value}, status=400)

        visitor_entry = visitorInOut_entry.visitortansid  # Access the related QitVisitormaster object directly
        if not visitor_entry:
            return Response({'Status': 400, 'StatusMsg': "Visitor master data not found",'APICode':APICodeClass.Visitor_Edit.value}, status=400)

        department_entry = QitDepartment.objects.filter(transid=did, cmptransid=cmpid).first()
        if not department_entry:
            return Response({'Status': 400, 'StatusMsg': "Department data not found",'APICode':APICodeClass.Visitor_Edit.value}, status=400)

        # Update visitor_entry fields
        visitor_entry.vname = body_data.get("vname", visitor_entry.vname)
        visitor_entry.phone1 = body_data.get("phone1", visitor_entry.phone1)
        visitor_entry.vcmpname = body_data.get("vcmpname", visitor_entry.vcmpname)
        visitor_entry.vlocation = body_data.get("vlocation", visitor_entry.vlocation)
        visitor_entry.save()

        # Update visitorInOut_entry fields
        visitorInOut_entry.cnctperson = body_data.get("cnctperson", visitorInOut_entry.cnctperson)
        visitorInOut_entry.cmpdepartmentid = department_entry
        visitorInOut_entry.purposeofvisit = body_data.get("purposeofvisit", visitorInOut_entry.purposeofvisit)
        visitorInOut_entry.timeslot = body_data.get("timeslot", visitorInOut_entry.timeslot)
        visitorInOut_entry.anyhardware = body_data.get("anyhardware", visitorInOut_entry.anyhardware)
        visitorInOut_entry.status = "P"
        visitorInOut_entry.save()

        return Response({'Status': 200, 'StatusMsg': "Visitor data saved successfully",'APICode':APICodeClass.Visitor_Edit.value}, status=200)

    except Exception as e:
        return Response({'Status': 400, 'StatusMsg': "An error occurred: {}".format(str(e)),'APICode':APICodeClass.Visitor_Edit.value}, status=400)
    # try:
    #     body_data = request.data
    #     if not body_data:
    #         return Response({'Status': 400, 'StatusMsg': "Payload required"}, status=400)  
        
    #     vid = body_data.get("visitor_id")
    #     cmpid = body_data.get("company_id")
    #     did = body_data.get("department_id")
        
    #     if not vid:
    #         return Response({'Status': 400, 'StatusMsg': "Visitor ID is required"}, status=400)  
    #     if not cmpid:
    #         return Response({'Status': 400, 'StatusMsg': "Company ID is required"}, status=400)  
    #     if not did:
    #         return Response({'Status': 400, 'StatusMsg': "Department ID is required"}, status=400)  
        
    #     companyEntry = QitCompany.objects.filter(transid=cmpid).first()
    #     if not companyEntry:
    #         return Response( {
    #             'isSaved':"N",
    #             'Status': 400,
    #             'StatusMsg': "Company not found"
    #         }, status=400)

    #     visitorInOut_entry = QitVisitorinout.objects.filter(transid=vid, cmptransid=cmpid).first()
    #     print("here")
    #     if not visitorInOut_entry:
    #         return Response({'Status': 400, 'StatusMsg': "Visitor data not found"}, status=400)
        
    #     print("here")
    #     if not visitorInOut_entry.createdby:
    #         return Response({'Status': 400, 'StatusMsg': "Visitor entry done by external"}, status=400)
 
    #     print("here :",visitorInOut_entry.visitortansid_transid)
    #     visitor_entry = QitVisitormaster.objects.filter(transid=visitorInOut_entry.visitortansid_transid).first()
    #     print("here :",visitorInOut_entry.visitortansid_transid)

    #     print(visitor_entry)

    #     if not visitor_entry:
    #         return Response({'Status': 400, 'StatusMsg': "Visitor data not found"}, status=400)
        
    #     department_entry = QitDepartment.objects.filter(transid=did,cmptransid=cmpid).first()
    #     if not department_entry:
    #         return Response({'Status': 400, 'StatusMsg': "Department data not found"}, status=400)
        
    #     visitor_entry.vname = body_data.get("vname")
    #     visitor_entry.phone1 = body_data.get("phone1")
    #     visitor_entry.vcmpname = body_data.get("vcmpname")
    #     visitor_entry.vlocation = body_data.get("vlocation")

    #     visitorInOut_entry.cnctperson = body_data.get("cnctperson")
    #     visitorInOut_entry.cmpdepartmentid = department_entry
    #     visitorInOut_entry.purposeofvisit = body_data.get("purposeofvisit")
    #     visitorInOut_entry.timeslot = body_data.get("timeslot")
    #     visitorInOut_entry.anyhardware = body_data.get("anyhardware")

    #     visitor_entry.save()
    #     visitorInOut_entry.save()

    #     return Response({'Status': 200, 'StatusMsg': "Checkout successfullyy"}, status=200)
        
    # except Exception as e:
    #     return Response({'Status': 400, 'StatusMsg': "An error occurred: {}".format(str(e))}, status=400)

@csrf_exempt
@api_view(["POST"])
def checkInVisitor(request):
    try:
        body_data = request.data
        if not body_data:
            return Response({'Status': 400, 'StatusMsg': "Payload required",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)  
        
        email = body_data.get("e_mail")
        cmpid = body_data.get("company_id")
        
        if not email:
            return Response({'Status': 400, 'StatusMsg': "Email is required",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)  
        if not cmpid:
            return Response({'Status': 400, 'StatusMsg': "Company ID is required",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)  
        today = now().date()
        companyEntry = QitCompany.objects.filter(transid=cmpid).first()
        if not companyEntry:
            return Response( {
                'isSaved':"N",
                'Status': 400,
                'StatusMsg': "Company not found",
                'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value
            }, status=400)

        visitor_entry = QitVisitormaster.objects.filter(e_mail=email, cmptransid=cmpid).first()
        if not visitor_entry:
            return Response({'Status': 400, 'StatusMsg': "Visitor data not found",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)
        
        inOutEntry = QitVisitorinout.objects.filter(visitortansid=visitor_entry.transid).order_by("-entrydate").first()

        if inOutEntry.timeslot.date() != today:
            return Response({'Status': 400, 'StatusMsg': "Visitor checkin entry not for today",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)
        
        if not inOutEntry:
            return Response({'Status': 400, 'StatusMsg': "Visitor checkin entry not found",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)
        
        if inOutEntry.status.upper() != "A":
            return Response({'Status': 400, 'StatusMsg': "Visitor status is not approve",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)
        if inOutEntry.checkinstatus != None and inOutEntry.checkinstatus.upper() == "I":
            return Response({'Status': 400, 'StatusMsg': "Visitor already checked In",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)
        
        if inOutEntry.checkinstatus != None and inOutEntry.checkinstatus.upper() == "O":
            return Response({'Status': 400, 'StatusMsg': "Visitor already checked out!!",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)
        if inOutEntry.createdby == None:
            return Response({'Status': 400, 'StatusMsg': "You can not been checkin by your self",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)
        inOutEntry.checkintime = datetime.now()
        inOutEntry.checkinstatus = "I"
        inOutEntry.save()

        return Response({'Status': 200, 'StatusMsg': "Checkin successfullyy",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=200)
        
    except Exception as e:
        return Response({'Status': 400, 'StatusMsg': "An error occurred: {}".format(str(e)),'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)

@csrf_exempt
@api_view(["POST"])
def send_email_notification(request):
    try:
        today = timezone.now().date()
        visitors_data = QitVisitorinout.objects.filter(
            timeslot__date=today,
            status='A'
        )
        print("visitors_to_remind : => ",visitors_data)
        if visitors_data.exists():
            for visitors_to_remind in visitors_data:
                cmpid = visitors_to_remind.cmptransid
                print("cmptransid : ",cmpid)
                statusLink = os.getenv("FRONTEND_URL") + '#/checkstatus/?cmpId=' + cmpid.qrstring
                verifyLink = os.getenv("FRONTEND_URL") +'#/Verify-Visitors'
                users = None
                users = QitUsermaster.objects.filter(username=visitors_to_remind.cnctperson,cmpdeptid=visitors_to_remind.cmpdepartmentid,cmptransid=cmpid)
                print("users : ",users)
                emails = []
                if users:
                    for data in users:
                        emails.append(data.e_mail)
                else:
                    users = QitUsermaster.objects.filter(cmpdeptid=visitors_to_remind.cmpdepartmentid,cmptransid=cmpid)
                    for data in users:
                        emails.append(data.e_mail)
                # emails.append(visitor['vEmail'])
                print("Emails : ",emails)
                print("visitors_to_remind.visitortansid.e_mail : ",visitors_to_remind.visitortansid.e_mail)
                visitor_dict = {
                'id': visitors_to_remind.transid,
                'vName': visitors_to_remind.visitortansid.vname,
                'vPhone1':visitors_to_remind.visitortansid.phone1,
                'vCmpname': visitors_to_remind.visitortansid.vcmpname,
                'vLocation': visitors_to_remind.visitortansid.vlocation,
                'deptId': visitors_to_remind.cmpdepartmentid,
                'deptName': visitors_to_remind.cmpdepartmentid,
                'vEmail': visitors_to_remind.visitortansid.e_mail,
                'state': visitors_to_remind.checkinstatus,
                'status': visitors_to_remind.status,
                'addedBy': visitors_to_remind.createdby,
                'cnctperson': visitors_to_remind.cnctperson,
                'timeslot': visitors_to_remind.timeslot,
                'purposeofvisit': visitors_to_remind.purposeofvisit,
                'reason': visitors_to_remind.reason
            }
                message1 =  send_reminder(visitor_dict,"Visiting company reminder",statusLink,"To ensure a smooth check-in process, please click here","CheckIn")
                message2 =  send_reminder(visitor_dict,"Visitor arrival reminder",verifyLink,"To verify a visitor, please click here","verify now")
                # print("emails : ==> ",emails)
                send_html_mail(f"reminder",message2,emails)
                send_html_mail(f"reminder",message1,[visitors_to_remind.visitortansid.e_mail])
                return Response({'Status': 200, 'StatusMsg': "Send successfullyy",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=200)
            else:
                print("No visitors found matching the update criteria.")
                return Response({'Status': 400, 'StatusMsg': "An error occurred: No visitors found matching the update criteria.",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)
        return Response({'Status': 400, 'StatusMsg': "An error occurred: No visitors found matching the update criteria.",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)
    except Exception as e:
        return Response({'Status': 400, 'StatusMsg': "An error occurred: {}".format(str(e)),'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)
    

def send_email_notification_email(visitor,departmentId,cmpid):
    try:
        # body_data = request.data
        # if not body_data:
        #     return Response({'Status': 400, 'StatusMsg': "Payload required",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)  
        
        # visitor = body_data.get("visitor")
        # departmentId = body_data.get("departmentId")
        # cmpid = body_data.get("cmpid")
        companyEntry = QitCompany.objects.filter(transid=cmpid).first()
        statusLink = os.getenv("FRONTEND_URL") + '#/checkstatus/?cmpId=' + companyEntry.qrstring
        verifyLink = os.getenv("FRONTEND_URL") +'#/Verify-Visitors'
        users = None
        users = QitUsermaster.objects.filter(username=visitor['cnctperson'],cmpdeptid=departmentId,cmptransid=cmpid)
        emails = []
        if users:
            for data in users:
                emails.append(data.e_mail)
        else:
            users = QitUsermaster.objects.filter(cmpdeptid=departmentId,cmptransid=cmpid)
            for data in users:
                emails.append(data.e_mail)
        # emails.append(visitor['vEmail'])
        
        message1 =  send_reminder(visitor,"Your registration to company",statusLink,"To ensure a smooth check-in process, please click here","CheckIn")
        message2 =  send_reminder(visitor,"New Visitor registered",verifyLink,"To verify a visitor, please click here","verify now")
        # print("emails : ==> ",emails)
        send_html_mail(f"reminder",message2,emails)
        send_html_mail(f"reminder",message1,[visitor['vEmail']])
        # return Response({'Status': 200, 'StatusMsg': "Send successfullyy",'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=200)
    except Exception as e:
        print("Error : ",str(e))
        # return Response({'Status': 400, 'StatusMsg': "An error occurred: {}".format(str(e)),'APICode':APICodeClass.Visitor_Mobile_ChkOutByV.value}, status=400)
