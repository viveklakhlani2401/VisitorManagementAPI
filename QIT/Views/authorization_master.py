from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from QIT.models import QitUsermaster, QitAuthenticationrule,QitCompany
from QIT.serializers import GetDataClassSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def SaveAuthRule(request):
    print(request.data)
    # serializer = GetDataClassSerializer(data=request.data)
    # if not serializer.is_valid():
    #     return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)


    logger.info("Received data: %s", request.data)
    serializer = GetDataClassSerializer(data=request.data)
    
    if not serializer.is_valid():
        logger.error("Invalid data: %s", serializer.errors)
        return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    useremail = data['useremail']
    user_role = data['userrole']
    cmptransid = data['cmptransid']
    module_classes = data['module_classes']


    # data = serializer.validated_data
    # useremail = data['useremail']
    # cmptransid = data['cmptransid']
    # module_classes = data['module_classes']
    
    try:
        logger.info("Calling AuthUserController: SaveAuthRule()")
        user = None
        cmptransidUser = None
        if 'COMPANY' in data['userrole'].upper():
            user = QitCompany.objects.filter(e_mail=useremail).first()
            cmptransidUser = user
        elif 'USER' in data['userrole'].upper():
            user = QitUsermaster.objects.filter(useremail=useremail).first()
            cmptransidUser = user.cmptransid
        if not user:
            logger.info("Calling AuthUserController saved rule: SaveAuthRule(): Error User not found")
            return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': 'User Not found..!!'}, status=status.HTTP_400_BAD_REQUEST)
        print(str(cmptransidUser.transid).strip(), "  ",str(cmptransid).strip())
        if str(cmptransidUser.transid).strip() != str(cmptransid).strip():
            logger.info("Calling AuthUserController saved rule: SaveAuthRule(): Error Invalid company user")
            return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': 'Invalid company user'}, status=status.HTTP_400_BAD_REQUEST)

        # user = QitUsermaster.objects.filter(useremail=useremail).first()

        # if not user:
        #     logger.info("Calling AuthUserController saved rule: SaveAuthRule(): Error User not found")
        #     return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': 'User Not found..!!'}, status=status.HTTP_400_BAD_REQUEST)

        ar_data = module_classes

        existing_rule = QitAuthenticationrule.objects.filter(user_id=user.transid).first()

        if existing_rule:
            print("ardata : ",ar_data)
            existing_rule.auth_rule_detail = ar_data
            existing_rule.save()
        else:
            new_rule = QitAuthenticationrule(user_id=user.transid,cmptransid=cmptransidUser, auth_rule_detail=ar_data,userrole=data['userrole'].upper())
            new_rule.save()

        logger.info("Calling AuthUserController saved rule: SaveAuthRule()")
        return Response({'StatusCode': '200', 'IsSaved': 'Y', 'StatusMsg': 'Saved Successfully!!!'}, status=status.HTTP_200_OK)
    except Exception as ex:
        print( str(ex))
        logger.error("Calling AuthUserController Error: SaveAuthRule() " + str(ex))
        return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
