from rest_framework import serializers
from .models import QitCompanymaster,QitOtp,QitUserlogin

class CompanyMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = QitCompanymaster
        fields = "__all__"

class GenerateOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = QitOtp
        fields = ["e_mail"]

class CompanyMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = QitCompanymaster
        fields = ['e_mail', 'password', 'businessname', 'businesslocation']
    
class CompanyMasterGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QitCompanymaster
        fields = ['e_mail', 'password', 'businessname', 'businesslocation','qrcodeid','status','entrydate']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = QitUserlogin
        fields = ['useremail','userrole']