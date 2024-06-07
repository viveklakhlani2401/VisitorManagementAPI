from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import QitCompany,QitOtp,QitUserlogin,QitDepartment,QitUsermaster

class CompanyMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = QitCompany
        fields = "__all__"

class GenerateOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = QitOtp
        fields = ["e_mail"]

class CompanyMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = QitCompany
        fields = ['e_mail', 'password', 'bname', 'blocation']

    def create(self, validated_data):
        # Encrypt the password
        validated_data['password'] = make_password(validated_data['password'])
        print(validated_data['password'])
        return super().create(validated_data)

class CompanyMasterGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QitCompany
        fields = ['transid','e_mail', 'password', 'bname', 'blocation','qrstring','status','entrydate']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = QitUserlogin
        fields = ['e_mail','userrole']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QitDepartment
        fields = ['transid','deptname','cmptransid']

        
class QitUsermasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = QitUsermaster
        fields = '__all__'

    def create(self, validated_data):
        # Encrypt the password
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.cmptransid = validated_data.get('cmptransid', instance.cmptransid)
        instance.cmpdeptid = validated_data.get('cmpdeptid', instance.cmpdeptid)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.useravatar = validated_data.get('useravatar', instance.useravatar)
        instance.changepassstatus = validated_data.get('changepassstatus', instance.changepassstatus)
        if 'password' in validated_data:
            instance.password = make_password(validated_data['password'])
        instance.save()
        return instance

class UserMasterDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = QitUsermaster
        fields = ['username','useremail', 'phone','cmpdeptid','gender','useravatar','changepassstatus']

class UserMasterResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QitUsermaster
        fields = ['password']

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.password = make_password(validated_data['password'])
        instance.save()
        return instance


class GetDataClassSerializer(serializers.Serializer):
    useremail = serializers.CharField(max_length=255)
    userrole = serializers.CharField(max_length=10)
    cmptransid = serializers.IntegerField()
    module_classes = serializers.JSONField()
