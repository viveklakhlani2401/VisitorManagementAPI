from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from QIT.models import QitUsermaster, QitAuthenticationrule,QitCompany
from QIT.serializers import GetDataClassSerializer,GetRuleClassSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def SaveAuthRule(request):
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

    try:
        logger.info("Calling authorization_master: SaveAuthRule()")
        cmpcheck = user = QitCompany.objects.filter(transid=cmptransid).first()
        if not cmpcheck:
            return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': 'Invalid company'}, status=status.HTTP_400_BAD_REQUEST)

        user = None
        cmptransidUser = None
        if 'COMPANY' in data['userrole'].upper():
            user = QitCompany.objects.filter(e_mail=useremail).first()
            if not user:
                logger.info("Calling authorization_master saved rule: GetAuthRule(): Error User not found")
                return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': 'Company Not found..!!'}, status=status.HTTP_400_BAD_REQUEST)
            cmptransidUser = user
        elif 'USER' in data['userrole'].upper():
            user = QitUsermaster.objects.filter(e_mail=useremail).first()
            if not user:
                logger.info("Calling authorization_master saved rule: GetAuthRule(): Error User not found")
                return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': 'User Not found..!!'}, status=status.HTTP_400_BAD_REQUEST)
            cmptransidUser = user.cmptransid
        if not user:
            logger.info("Calling authorization_master saved rule: SaveAuthRule(): Error User not found")
            return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': 'User Not found..!!'}, status=status.HTTP_400_BAD_REQUEST)
        if str(cmptransidUser.transid).strip() != str(cmptransid).strip():
            logger.info("Calling authorization_master saved rule: SaveAuthRule(): Error Invalid company user")
            return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': 'Invalid company user'}, status=status.HTTP_400_BAD_REQUEST)

        ar_data = module_classes

        existing_rule = QitAuthenticationrule.objects.filter(user_id=user.transid).first()

        if existing_rule:
            existing_rule.auth_rule_detail = ar_data
            existing_rule.save()
        else:
            new_rule = QitAuthenticationrule(user_id=user.transid,cmptransid=cmptransidUser, auth_rule_detail=ar_data,userrole=data['userrole'].upper())
            new_rule.save()

        logger.info("Calling authorization_master saved rule: SaveAuthRule()")
        return Response({'StatusCode': '200', 'IsSaved': 'Y', 'StatusMsg': 'Saved Successfully!!!'}, status=status.HTTP_200_OK)
    except Exception as ex:
        logger.error("Calling authorization_master Error: SaveAuthRule() " + str(ex))
        return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def GetAuthRule(request):
    logger.info("Received data: %s", request.data)
    serializer = GetRuleClassSerializer(data=request.data)
    
    if not serializer.is_valid():
        logger.error("Invalid data: %s", serializer.errors)
        return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    useremail = data['useremail']
    user_role = data['userrole']
    cmptransid = data['cmptransid']
    
    try:
        logger.info("Calling authorization_master: GetAuthRule()")
        cmpcheck = user = QitCompany.objects.filter(transid=cmptransid).first()
        if not cmpcheck:
            return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': 'Invalid company'}, status=status.HTTP_400_BAD_REQUEST)

        user = None
        cmptransidUser = None
        if 'COMPANY' in data['userrole'].upper():
            user = QitCompany.objects.filter(e_mail=useremail).first()
            if not user:
                logger.info("Calling authorization_master saved rule: GetAuthRule(): Error User not found")
                return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': 'Company Not found..!!'}, status=status.HTTP_400_BAD_REQUEST)
            cmptransidUser = user
        elif 'USER' in data['userrole'].upper():
            user = QitUsermaster.objects.filter(e_mail=useremail).first()
            if not user:
                logger.info("Calling authorization_master saved rule: GetAuthRule(): Error User not found")
                return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': 'User Not found..!!'}, status=status.HTTP_400_BAD_REQUEST)
            cmptransidUser = user.cmptransid
        if not user:
            logger.info("Calling authorization_master saved rule: GetAuthRule(): Error User not found")
            return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': 'User Not found..!!'}, status=status.HTTP_400_BAD_REQUEST)
        if str(cmptransidUser.transid).strip() != str(cmptransid).strip():
            logger.info("Calling authorization_master saved rule: GetAuthRule(): Error Invalid company user")
            return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': 'Invalid company user'}, status=status.HTTP_400_BAD_REQUEST)

        existing_rule = QitAuthenticationrule.objects.filter(user_id=user.transid).first()
        if existing_rule:
            return Response({'StatusCode': '200', 'IsSaved': 'Y', 'Notification_Rule': existing_rule.auth_rule_detail}, status=status.HTTP_200_OK)
        else:
            return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': 'No Rule Found'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        logger.error("Calling authorization_master Error: GetAuthRule() " + str(ex))
        return Response({'StatusCode': '400', 'IsSaved': 'N', 'StatusMsg': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
