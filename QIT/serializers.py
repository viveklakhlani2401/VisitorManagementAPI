from rest_framework import serializers
from .models import QitCompanymaster,QitOtp
from django.contrib.auth.hashers import make_password
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
    
    def create(self, validated_data):
        # Encrypt the password
        validated_data['password'] = make_password(validated_data['password'])
        print(validated_data['password'])
        return super().create(validated_data)


class CompanyMasterGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QitCompanymaster
        fields = ['e_mail', 'password', 'businessname', 'businesslocation','qrcodeid','status','entrydate']