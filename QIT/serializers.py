from rest_framework import serializers
from .models import Company_Master, OTP

class CompanyMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company_Master
        fields = "__all__"

class GenerateOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ["E_Mail"]