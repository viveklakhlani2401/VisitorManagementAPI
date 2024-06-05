from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from QIT.models import QitUsermaster,QitUserlogin
from QIT.serializers import QitUsermasterSerializer,UserMasterDataSerializer,UserMasterResetSerializer
from .common import create_userlogin
from django.contrib.auth.hashers import make_password
@api_view(['POST'])
def save_user(request):
    try:
        body_data = request.data
        serializer = QitUsermasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            userlogin = QitUserlogin(useremail=body_data["useremail"], password=make_password(body_data["password"]), userrole="USER")
            userlogin.save()
            return Response({
                    'Status':status.HTTP_201_CREATED,
                    'StatusMsg':"User Save Successfully..!!"
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
                    'Status':400,
                    'StatusMsg':str(e)
                })

@api_view(['GET'])
def get_user(request,cmpId):
    try:
        users = QitUsermaster.objects.filter(cmptransid=cmpId)
        serializer = QitUsermasterSerializer(users, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({
                    'Status':400,
                    'StatusMsg':str(e)
                })

@api_view(['GET'])
def get_user_by_id(request, cmpId, transid):
    try:
        user = QitUsermaster.objects.get(cmptransid=cmpId, transid=transid)
    except QitUsermaster.DoesNotExist:
        return Response({'Status': 404, 'StatusMsg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserMasterDataSerializer(user)
    return Response(serializer.data)
 
@api_view(['PUT'])
def update_user(request,cmpId, transid):
    try:
        user = QitUsermaster.objects.get(cmptransid=cmpId, transid=transid)
    except QitUsermaster.DoesNotExist:
        return Response({
                    'Status':status.HTTP_404_NOT_FOUND,
                    'StatusMsg':"No data found..!!"
                },status=status.HTTP_404_NOT_FOUND)
    serializer = QitUsermasterSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
                'Status':status.HTTP_404_NOT_FOUND,
                'StatusMsg':"User Data Updated!!"
            },status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT'])
# def reset_user_password(request,cmpId, transid):
#     try:
#         user = QitUsermaster.objects.get(cmptransid=cmpId, transid=transid)
#     except QitUsermaster.DoesNotExist:
#         return Response({
#                     'Status':status.HTTP_404_NOT_FOUND,
#                     'StatusMsg':"No data found..!!"
#                 },status=status.HTTP_404_NOT_FOUND)
#     serializer = UserMasterResetSerializer(user, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({
#                 'Status':status.HTTP_404_NOT_FOUND,
#                 'StatusMsg':"User Data Updated!!"
#             },status=status.HTTP_404_NOT_FOUND)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_user(request, cmpId, transid):
    try:
        user = QitUsermaster.objects.get(cmptransid=cmpId, transid=transid)
    except QitUsermaster.DoesNotExist:
        return Response({
                    'Status':status.HTTP_404_NOT_FOUND,
                    'StatusMsg':"No data found..!!"
                },status=status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response({
                    'Status':200,
                    'StatusMsg':"User Data Deleted!!"
                })
