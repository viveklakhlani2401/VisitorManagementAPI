from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from QIT.serializers import QitVisitorinoutGETSerializer
from QIT.models import QitVisitorinout,QitCompany
from django.core.cache import cache
from datetime import datetime,timedelta
from QIT.Views import common
from django.utils import timezone
from django.utils.timezone import make_aware

# get all visior data for company
@csrf_exempt
@api_view(["POST"])
def GetVisitorReport(request):
    try:
        body_data = request.data
        cid = body_data.get("cid")
        fdate = body_data.get("fdate")
        tdate = body_data.get("tdate")
        if not body_data:
            return Response({
                'Status': 400,
                'StatusMsg': "Payload required..!!"
            },status=400)  
        if not cid:
            return Response({'Status': 400, 'StatusMsg': "Company Id requied..!!"}, status=400)

        companyEntry = QitCompany.objects.filter(transid=cid).first()
        if not companyEntry:
            return Response( {
                'Status': 400,
                'StatusMsg': "Company not found..!!"
            }, status=400)

        from_date = datetime.strptime(fdate, '%Y-%m-%d')
        to_date = datetime.strptime(tdate, '%Y-%m-%d')+ timedelta(days=1)

        # Make them timezone-aware
        from_date = make_aware(from_date)
        to_date = make_aware(to_date)

        queryset = QitVisitorinout.objects.filter(
            cmptransid=cid,
            entrydate__range=(from_date, to_date)
        ).order_by('-entrydate')
        if not queryset:
            return Response({'Status': 400, 'StatusMsg': "No data..!!"}, status=400)
        serializer = QitVisitorinoutGETSerializer(queryset, many=True)
        return Response(serializer.data,status=200)
    except Exception as e:
        return Response({'Status': 400, 'StatusMsg': str(e)}, status=400)
