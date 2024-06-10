from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import QitCompany,QitOtp,QitUserlogin,QitDepartment,QitUsermaster,QitVisitormaster,QitVisitorinout

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


class GetRuleClassSerializer(serializers.Serializer):
    useremail = serializers.CharField(max_length=255)
    userrole = serializers.CharField(max_length=10)
    cmptransid = serializers.IntegerField()

class SetNotificationClassSerializer(serializers.Serializer):
    module = serializers.CharField(max_length=50)
    sender_email = serializers.CharField(max_length=255)
    sender_role = serializers.CharField(max_length=50)
    notification_text = serializers.CharField(max_length=255)
    cmptransid = serializers.IntegerField()

class GetNotificationClassSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    cmptransid = serializers.IntegerField()

class ReadNotificationClassSerializer(serializers.Serializer):
    transid = serializers.IntegerField()
    email = serializers.CharField(max_length=255)
    cmptransid = serializers.IntegerField()

class QitVisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = QitVisitormaster
        fields = '__all__'

    # def to_representation(self, instance):
    #     print("here")
    #     representation = super().to_representation(instance)
    #     print("here")
    #     print(instance.visitortansid)
    #     visitormaster = instance.visitortansid
    #     # representation['visitor_transid'] = visitormaster.transid
    #     representation['vName'] = visitormaster.vname
    #     representation['visitor_phone1'] = visitormaster.phone1
    #     representation['visitor_cmpname'] = visitormaster.vcmpname
    #     representation['visitor_location'] = visitormaster.vlocation
    #     representation['visitor_email'] = visitormaster.e_mail
    #     representation['visitor_cmptransid'] = visitormaster.cmptransid_id

    #     return representation


class QitVisitorinoutPOSTSerializer(serializers.ModelSerializer):
    vname = serializers.CharField(write_only=True, max_length=45)
    phone1 = serializers.CharField(write_only=True, max_length=45, allow_blank=True, allow_null=True)
    vcmpname = serializers.CharField(write_only=True, max_length=45)
    vlocation = serializers.CharField(write_only=True, max_length=45)
    e_mail = serializers.CharField(write_only=True, max_length=45)
    cmptransid = serializers.IntegerField(write_only=True)

    class Meta:
        model = QitVisitorinout
        fields = [
            'vavatar', 'cnctperson', 'cmpdepartmentid', 'timeslot', 'anyhardware',
            'purposeofvisit', 'cmptransid', 'reason', 'checkintime', 'checkouttime',
            'createdby', 'vname', 'phone1', 'vcmpname', 
            'vlocation', 'e_mail'
        ]
        # fields = '__all__'

    def create(self, validated_data):

        if validated_data.get("createdby"):
            try:
                userEntry = QitUserlogin.objects.get(transid=validated_data.get("createdby"))
            except QitUserlogin.DoesNotExist:
                raise serializers.ValidationError({"statusMsg":"Invalid created by user id..!!"})

        try:
            # print(validated_data.pop('cmptransid'))
            company = QitCompany.objects.get(transid=validated_data.pop('cmptransid'))
        except QitCompany.DoesNotExist:
            raise serializers.ValidationError({"statusMsg":"company_id not found."})
        
        # try:
        #     print(validated_data.get('cmpdepartmentid'))
        #     dept = QitDepartment.objects.get(transid=validated_data.get('cmpdepartmentid'))
        # except QitDepartment.DoesNotExist:
        #     raise serializers.ValidationError({"statusMsg":"department_id not found."})

        # visitormaster_data = {
        #     'vname': validated_data.pop('vname'),
        #     'phone1': validated_data.pop('phone1'),
        #     'vcmpname': validated_data.pop('vcmpname'),
        #     'vlocation': validated_data.pop('vlocation'),
        #     'e_mail': validated_data.pop('e_mail'),
        #     'cmptransid': company,
        # }
        # visitormaster = QitVisitormaster.objects.create(**visitormaster_data).

        email = validated_data.pop('e_mail')
        visitormaster_data = {
            'vname': validated_data.pop('vname'),
            'phone1': validated_data.pop('phone1', None),
            'vcmpname': validated_data.pop('vcmpname'),
            'vlocation': validated_data.pop('vlocation'),
            'e_mail': email,
            'cmptransid': company,
        }

        visitormaster, created = QitVisitormaster.objects.update_or_create(
            e_mail=email,
            cmptransid=company,
            defaults=visitormaster_data
        )
        validated_data['visitortansid'] = visitormaster
        validated_data['status'] = 'P'
        validated_data['checkinstatus'] = None
        validated_data['cmptransid'] = company
        validated_data['cmpdepartmentid'] = validated_data.get('cmpdepartmentid')
        visitorinout = QitVisitorinout.objects.create(**validated_data)
        return visitorinout

class QitVisitorinoutGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = QitVisitorinout
        fields = ['transid','cnctperson','cmpdepartmentid','timeslot','purposeofvisit','checkinstatus','reason','status','entrydate','createdby','checkintime']

      
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        departmentMaster = instance.cmpdepartmentid
        visitormaster = instance.visitortansid

        # Debug statements
        print("Type of entry_date:", type(representation['entrydate']))
        print("Value of entry_date:", representation['entrydate'])
        
        # Manually add fields from QitVisitormaster to the representation
        # representation['vId'] = visitormaster.transid
        representation['id'] = representation.pop("transid")
        representation['vName'] = visitormaster.vname
        representation['vPhone1'] = visitormaster.phone1
        representation['vCmpname'] = visitormaster.vcmpname
        representation['vLocation'] = visitormaster.vlocation
        representation['vEmail'] = visitormaster.e_mail
        representation['deptId'] = representation.pop("cmpdepartmentid")
        representation['deptName'] = departmentMaster.deptname
        status_mapping = {
            'P': 'Pending',
            'A': 'Approved',
            'R': 'Rejected'
        }
        representation['state'] = status_mapping.get(representation.pop('status'), None)
        state_mapping = {
            'I': 'Check in',
            'O': 'Check Out'
        }
        representation['status'] = state_mapping.get(representation.pop('checkinstatus'), None)
        representation['addedBy'] = 'Company' if representation.pop("createdby") else 'External'
        representation['cnctperson'] =  representation.pop("cnctperson") 
        representation['timeslot'] =  representation.pop("timeslot") 
        representation['purposeofvisit'] =  representation.pop("purposeofvisit") 
        representation['reason'] =  representation.pop("reason") 
        entryDate = representation.pop('entrydate')
        checkinDate = representation.pop('checkintime')
        representation['sortDate'] = checkinDate if checkinDate else entryDate
        # representation['vCmptransid'] = visitormaster.cmptransid_id

        return representation
