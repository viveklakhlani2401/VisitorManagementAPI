from rest_framework.views import APIView 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from QIT.models import QitDepartment,QitCompany
from QIT.serializers import DepartmentSerializer
from rest_framework.exceptions import NotFound
from django.db import IntegrityError
from QIT.utils.APICode import APICodeClass

# @csrf_exempt
# @api_view(["POST"])
# def SaveDepartment(request):
#     try:
#         reqData = request.data
#         cid = reqData["company_id"]
#         cmpEntry = QitCompany.objects.filter(transid=cid).first()
#         if not cmpEntry:
#             return Response({
#                 'is_save':"N",
#                 'Status':400,
#                 'StatusMsg':"Company not found..!!"
#             })
#         res = QitDepartment.objects.create(deptname=reqData["dept_name"],cmptransid=cmpEntry)
#         if res:
#             return Response({
#                 'is_save':"Y",
#                 'Status':200,
#                 'StatusMsg':"Department data saved..!!"
#             })
#         else:
#             return Response({
#                 'is_save':"N",
#                 'Status':400,
#                 'StatusMsg':"Error while saving data..!!"
#             })
#     except Exception as e:
#         return Response({
#             'is_save':"N",
#             'Status':400,
#             'StatusMsg':e
#         })


@csrf_exempt
@api_view(["POST"])
def SaveDepartment(request):
    try:
        reqData = request.data
        cid = reqData["company_id"]
        cmpEntry = QitCompany.objects.filter(transid=cid).first()
        if not cmpEntry:
            return Response({
                'is_save': "N",
                'Status': 400,
                'StatusMsg': "Company not found..!!",
                'APICode':APICodeClass.Department_Add.value
            })
        
        dept_name = reqData["dept_name"]
        # Check if the department with the same name already exists for the given company (case-insensitive)
        existing_dept = QitDepartment.objects.filter(cmptransid=cmpEntry, deptname__iexact=dept_name).first()
        if existing_dept:
            return Response({
                'is_save': "N",
                'Status': 400,
                'StatusMsg': "Department with the same name already exists..!!",
                'APICode':APICodeClass.Department_Add.value
            },status=400)

        res = QitDepartment.objects.create(deptname=dept_name, cmptransid=cmpEntry)
        if res:
            return Response({
                'is_save': "Y",
                'Status': 200,
                'StatusMsg': "Department data saved..!!",
                'APICode':APICodeClass.Department_Add.value
            })
        else:
            return Response({
                'is_save': "N",
                'Status': 400,
                'StatusMsg': "Error while saving data..!!",
                'APICode':APICodeClass.Department_Add.value
            },status=400)
    except Exception as e:
        return Response({
            'is_save': "N",
            'Status': 400,
            'StatusMsg': str(e),
            'APICode':APICodeClass.Department_Add.value
        },status=400)

@csrf_exempt
@api_view(["GET"])
def GetAllDeptByCId(request,cid):
    # print(request.query_params.get("cid"))
    try:
        # cid = request.query_params.get("cid")
        if not cid:
            deptData = DepartmentSerializer(QitDepartment.objects.all(),many=True)
            return Response({
                'Data':deptData.data,
                'APICode':APICodeClass.Department_Get.value
            })
        else:
            cmpEntry = QitCompany.objects.filter(transid=cid).first()
            if not cmpEntry:
                raise NotFound(detail="Company data not found..!!",code=400)
            serializedData = QitDepartment.objects.filter(cmptransid=cmpEntry)
            if not serializedData:
                raise NotFound(detail="Data not found..!!",code=400)
            res = DepartmentSerializer(serializedData,many=True)
            return Response({
                'Data':res.data,
                'APICode':APICodeClass.Department_Get.value
            })
    except NotFound as e:
        return Response({'Status': 400, 'StatusMsg': str(e)}, status=400)
    except Exception as e:
        return Response({
            'Status':400,
            'StatusMsg':e,
            'APICode':APICodeClass.Department_Get.value
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
        
        cmpEntry = QitCompany.objects.filter(transid=reqData["cmptransid"]).first()
        if not cmpEntry:
            return Response({
                'is_save': "N",
                'Status': 400,
                'StatusMsg': "Company not found..!!",
                'APICode':APICodeClass.Department_Edit.value
            })
        
        # Check if the department with the same name already exists for the given company (case-insensitive)
        existing_dept = QitDepartment.objects.filter(cmptransid=reqData["cmptransid"], deptname__iexact=reqData["deptname"]).first()
        if existing_dept:
            return Response({
                'is_save': "N",
                'Status': 400,
                'StatusMsg': "Department with the same name already exists..!!",
                'APICode':APICodeClass.Department_Edit.value
            },status=400)
        
        deptData = QitDepartment.objects.filter(transid = reqData["transid"],cmptransid=reqData["cmptransid"]).first()
        if not deptData:
            raise NotFound(detail="Department data not found..!!",code=400)
        serialized_data = DepartmentSerializer(deptData, data=reqData, partial=True)
        if serialized_data.is_valid():
            serialized_data.save()
        return Response({
            'is_save':"Y",
            'Status':200,
            'StatusMsg':"Department data updated..!!",
            'APICode':APICodeClass.Department_Edit.value
        })
    except NotFound as e:
        return Response({
            'Status': 400, 
            'StatusMsg': str(e),
            'APICode':APICodeClass.Department_Edit.value
        }, status=400)
    except Exception as e:
        return Response({
            'Status':400,
            'StatusMsg':e,
            'APICode':APICodeClass.Department_Edit.value
        },status=400)


@csrf_exempt
@api_view(["DELETE"])
def DeleteDepartment(request, did, cid):
    try:
        if not did:
            raise NotFound(detail="Department Id is required..!!")
        if not cid:
            raise NotFound(detail="Company Id is required..!!")

        try:
            cmpEntry = QitCompany.objects.get(transid=cid)
        except QitCompany.DoesNotExist:
            return Response({
                'Status': 400, 
                'StatusMsg': "Company not found..!!",
                'APICode':APICodeClass.Department_Delete.value
            }, status=400)

        try:
            deptEntry = QitDepartment.objects.get(transid=did, cmptransid=cmpEntry)
        except QitDepartment.DoesNotExist:
            return Response({
                'Status': 400, 
                'StatusMsg': "Department not found..!!",
                'APICode':APICodeClass.Department_Delete.value
            }, status=400)

        try:
            deptEntry.delete()
            return Response({
                'Status': 200,
                'StatusMsg': "Department deleted..!!",
                'APICode':APICodeClass.Department_Delete.value
            }, status=200)
        except IntegrityError as e:
            # Check if the error is due to foreign key constraint violation
            if 'foreign key constraint fails'.upper() in str(e).upper():
                return Response({
                    'Status': 400,
                    'StatusMsg': "Department already in use..!!",
                    'APICode':APICodeClass.Department_Delete.value
                }, status=400)
            else:
                return Response({
                    'Status': 400,
                    'StatusMsg': str(e),
                    'APICode':APICodeClass.Department_Delete.value
                }, status=400)
    except NotFound as e:
        return Response({
            'Status': 400, 
            'StatusMsg': str(e),
            'APICode':APICodeClass.Department_Delete.value
        }, status=400)
    except Exception as e:
        return Response({
            'Status': 400,
            'StatusMsg': str(e),
            'APICode':APICodeClass.Department_Delete.value
        }, status=400)
