from rest_framework.views import APIView 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from QIT.models import QitDepartmentmaster,QitCompanymaster
from QIT.serializers import DepartmentSerializer
from rest_framework.exceptions import NotFound

@csrf_exempt
@api_view(["POST"])
def SaveDepartment(request):
    print(request.data)
    try:
        reqData = request.data
        cid = reqData["company_id"]
        cmpEntry = QitCompanymaster.objects.filter(transid=cid).first()
        if not cmpEntry:
            return Response({
                'is_save':"N",
                'Status':400,
                'StatusMsg':"Company not found..!!"
            })
        res = QitDepartmentmaster.objects.create(deptname=reqData["dept_name"],cmptransid=cmpEntry)
        if res:
            return Response({
                'is_save':"Y",
                'Status':200,
                'StatusMsg':"Department data saved..!!"
            })
        else:
            return Response({
                'is_save':"N",
                'Status':400,
                'StatusMsg':"Error while saving data..!!"
            })
    except Exception as e:
        return Response({
            'is_save':"N",
            'Status':400,
            'StatusMsg':e
        })


@csrf_exempt
@api_view(["GET"])
def GetAllDeptByCId(request,cid):
    # print(request.query_params.get("cid"))
    try:
        # cid = request.query_params.get("cid")
        if not cid:
            deptData = DepartmentSerializer(QitDepartmentmaster.objects.all(),many=True)
            return Response(deptData.data)
        else:
            cmpEntry = QitCompanymaster.objects.filter(transid=cid).first()
            if not cmpEntry:
                raise NotFound(detail="Company data not found..!!",code=400)
            serializedData = QitDepartmentmaster.objects.filter(cmptransid=cmpEntry)
            if not serializedData:
                raise NotFound(detail="Data not found..!!",code=400)
            res = DepartmentSerializer(serializedData,many=True)
            return Response(res.data)
    except NotFound as e:
        return Response({'Status': 400, 'StatusMsg': str(e)}, status=400)
    except Exception as e:
        return Response({
            'Status':400,
            'StatusMsg':e
        },status=400)

@csrf_exempt
@api_view(["PUT"])
def EditDepartment(request):
    try:
        reqData = request.data
        if not reqData.get("transid"):
            raise NotFound(detail="transid is required..!!",code=400)
        if not reqData.get("deptname"):
            raise NotFound(detail="deptname is required..!!",code=400)
        if not reqData.get("cmptransid"):
            raise NotFound(detail="cmptransid is required..!!",code=400)
        deptData = QitDepartmentmaster.objects.filter(transid = reqData["transid"],cmptransid=reqData["cmptransid"]).first()
        if not deptData:
            raise NotFound(detail="Department data not found..!!",code=400)
        serialized_data = DepartmentSerializer(deptData, data=reqData, partial=True)
        if serialized_data.is_valid():
            serialized_data.save()
        return Response({
            'is_save':"Y",
            'Status':200,
            'StatusMsg':"Department data updated..!!"
        })
    except NotFound as e:
        return Response({'Status': 400, 'StatusMsg': str(e)}, status=400)
    except Exception as e:
        return Response({
            'Status':400,
            'StatusMsg':e
        },status=400)


@csrf_exempt
@api_view(["DELETE"])
def DeleteDepartment(request,did,cid):
    try:
        if not did:
            raise NotFound(detail="Department Id is required..!!")
        if not cid:
            raise NotFound(detail="Company Id is required..!!")
        deptEntry = QitDepartmentmaster.objects.get(transid=did,cmptransid=cid)
        if not deptEntry:
            raise NotFound(detail="Department not found..!!")
        res = deptEntry.delete()
        if res:
            return Response({
                'Status':200,
                'StatusMsg':"Department deleted..!!"
            },status=200)
        else:
            return Response({
                'Status':400,
                'StatusMsg':"Error while delete department data..!!"
            },status=400)
    except NotFound as e:
        return Response({'Status': 400, 'StatusMsg': str(e)}, status=400)
    except Exception as e:
        return Response({
            'Status':400,
            'StatusMsg':e
        },status=400)
