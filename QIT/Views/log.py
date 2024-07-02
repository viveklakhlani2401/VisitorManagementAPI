from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from QIT.serializers import QitAPILogSerializer
from QIT.models import QitCompany,QitApiLog
from django.core.cache import cache
from datetime import datetime
from QIT.Views import common
from django.utils import timezone
from django.utils.timezone import make_aware
import json

@csrf_exempt
@api_view(["POST"])
def save_log(request):
    is_saved = "N"
    try:
        payload = json.loads(request.body)
 
        module = payload.get('Module')
        controller_name = payload.get('ControllerName')
        method_name = payload.get('MethodName')
        log_level = payload.get('LogLevel')
        log_message = payload.get('LogMessage')
        json_payload = payload.get('jsonPayload')
        login_user = payload.get('LoginUser')
        cmp_id = payload.get('Company_Id')
        form_id = payload.get("form_id")
        cmpEntry = 0
        if module!="Login" :
            cmpEntry = QitCompany.objects.filter(transid=cmp_id).first()
            # cmpEntry = cmpEntry.transid
            if not cmpEntry:
                return Response({"Status": "400", "IsSaved": is_saved, "StatusMsg": "Invalid Company_Id"}, status=400)
 
        if not module or module.strip() == "" or module.lower() == "string":
            print("here")
            return Response({"Status": "400", "IsSaved": is_saved, "StatusMsg": "Provide Module"}, status=400)
 
        if not controller_name or controller_name.strip() == "" or controller_name.lower() == "string":
            return Response({"Status": "400", "IsSaved": is_saved, "StatusMsg": "Provide Controller"}, status=400)
 
        if not method_name or method_name.strip() == "" or method_name.lower() == "string":
            return Response({"Status": "400", "IsSaved": is_saved, "StatusMsg": "Provide Method"}, status=400)
 
        if not log_level or log_level.upper() not in ["I", "S", "E"]:
            return Response({"Status": "400", "IsSaved": is_saved, "StatusMsg": "LogLevel Values : I:Information/S:Success/E:Error"}, status=400)
 
        if not log_message or log_message.strip() == "" or log_message.lower() == "string":
            return Response({"Status": "400", "IsSaved": is_saved, "StatusMsg": "Provide Log Message"}, status=400)
 
        # if not login_user or login_user.strip() == "" or login_user.lower() == "string":
        #     print(login_user)
        #     return Response({"Status": "400", "IsSaved": is_saved, "StatusMsg": "Provide Login User"}, status=400)
 
        log = QitApiLog(
            module=module,
            viewname=controller_name,
            methodname=method_name,
            loglevel=log_level,
            logmessage=log_message,
            jsonpayload=json_payload,
            loginuser=login_user,
            cmptransid=cmp_id,
            error_id=form_id
        )
        print(log.error_id)
        log.save()
 
        is_saved = "Y"
 
        return Response({"Status": "200", "IsSaved": is_saved, "StatusMsg": "Saved Successfully!!!"}, status=200)
 
    except Exception as ex:
        # logger.error("Error in save_log: %s", ex)
        return Response({"Status": "400", "IsSaved": is_saved, "StatusMsg": str(ex)}, status=400)
    
# @csrf_exempt
# @api_view(["GET"])
# def Get_log(request, cid):
#     print(cid)
#     try:
#         cmpEntry = QitCompany.objects.filter(transid=cid).first()
#         if not cmpEntry:
#             return Response({"Status": "400", "StatusMsg": "Invalid Company_Id"}, status=400)
#         logEntry = QitApiLog.objects.filter(cmptransid=cmpEntry)
#         print(logEntry)
#         if not logEntry.exists():
#             return Response({"Status": "400", "StatusMsg": "No Data..!!"}, status=400)
#         serialized_data = QitAPILogSerializer(logEntry, many=True)
#         return Response(serialized_data.data)
#     except Exception as e :
#         return Response({"Status": "400", "StatusMsg": str(e)}, status=400)
    
from django.db.models import Q
from django.utils.dateparse import parse_datetime
@csrf_exempt
@api_view(["POST"])
def Get_log(request):
    try:
        payload = json.loads(request.body)
 
        cid = payload.get("cid")
        module = payload.get('Module')
        viewname = payload.get('viewname')
        methodname = payload.get('methodname')
        loglevel = payload.get('loglevel')
        loginuser = payload.get('LoginUser')
        fdate = payload.get("fdate")
        tdate = payload.get("tdate")

        if not loginuser:
            return Response({"Status": "400", "StatusMsg": "Please provide loginuser"}, status=400)


        cmpEntry = QitCompany.objects.filter(transid=cid).first()
        if not cmpEntry:
            return Response({"Status": "400", "StatusMsg": "Invalid Company_Id"}, status=400)

        query = Q(cmptransid=cid)
       
        if module:
            query &= Q(module=module)
        if viewname:
            query &= Q(viewname__icontains=viewname)
        if methodname:
            query &= Q(methodname__icontains=methodname)
        if loginuser:
            if loginuser != "Admin":
                query &= Q(loginuser=loginuser)
        if loglevel:
            if loglevel != "I" and loglevel != "S" and loglevel != "E":
                return Response({"Status": "400", "StatusMsg": "Loglevel format should be I : Information ,S : Success ,E : Error "}, status=400)
            query &= Q(loglevel=loglevel)
        if fdate and tdate:
            from_date = datetime.strptime(fdate, '%Y-%m-%d')
            to_date = datetime.strptime(tdate, '%Y-%m-%d')

            from_date = make_aware(from_date)
            to_date = make_aware(to_date)
            if from_date and to_date:
                query &= Q(entrydate__range=(from_date, to_date))
            else:
                return Response({"Status": "400", "StatusMsg": "Invalid date format"}, status=400)

        logEntry = QitApiLog.objects.filter(query).order_by('-entrydate')

        if not logEntry.exists():
            return Response({"Status": "400", "StatusMsg": "No Data..!!"}, status=400)

        serialized_data = QitAPILogSerializer(logEntry, many=True)
        return Response(serialized_data.data)

    except Exception as e:
        return Response({"Status": "400", "StatusMsg": str(e)}, status=400)
