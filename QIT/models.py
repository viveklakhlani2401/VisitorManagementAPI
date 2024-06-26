# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class QitApiLog(models.Model):
    transid = models.AutoField(db_column='TransId', primary_key=True)  # Field name made lowercase.
    module = models.CharField(db_column='Module', max_length=200, blank=True, null=True)  # Field name made lowercase.
    viewname = models.CharField(db_column='ViewName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    methodname = models.CharField(db_column='MethodName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    loglevel = models.CharField(db_column='LogLevel', max_length=2, blank=True, null=True)  # Field name made lowercase.
    logmessage = models.TextField(db_column='LogMessage', blank=True, null=True)  # Field name made lowercase.
    jsonpayload = models.CharField(db_column='JsonPayload', max_length=45, blank=True, null=True)  # Field name made lowercase.
    loginuser = models.CharField(db_column='LoginUser', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cmptransid = models.ForeignKey('QitCompany', models.DO_NOTHING, db_column='CmpTransId', blank=True, null=True)  # Field name made lowercase.
    entrydate = models.DateTimeField(db_column='EntryDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QIT_API_Log'


class QitAuthenticationrule(models.Model):
    authentication_rule_id = models.AutoField(db_column='Authentication_Rule_ID', primary_key=True)  # Field name made lowercase.
    user_id = models.IntegerField(db_column='User_ID')  # Field name made lowercase.
    cmptransid = models.ForeignKey('QitCompany', models.DO_NOTHING, db_column='CmpTransID')  # Field name made lowercase.
    auth_rule_detail = models.TextField(db_column='Auth_Rule_Detail')  # Field name made lowercase.
    userrole = models.CharField(db_column='userRole', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QIT_AuthenticationRule'


class QitCompany(models.Model):
    transid = models.AutoField(db_column='TransId', primary_key=True)  # Field name made lowercase.
    e_mail = models.CharField(db_column='E_Mail', unique=True, max_length=50)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=100)  # Field name made lowercase.
    bname = models.CharField(db_column='BName', max_length=200)  # Field name made lowercase.
    blocation = models.CharField(db_column='BLocation', max_length=500)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=50, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50, blank=True, null=True)  # Field name made lowercase.
    zipcode = models.CharField(db_column='ZipCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    address1 = models.CharField(db_column='Address1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address2 = models.CharField(db_column='Address2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='Phone1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    phone2 = models.CharField(db_column='Phone2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    qrstring = models.CharField(db_column='QRString', max_length=100)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=2)  # Field name made lowercase.
    isactive = models.CharField(db_column='IsActive', max_length=2)  # Field name made lowercase.
    cmplogo = models.TextField(db_column='CmpLogo', blank=True, null=True)  # Field name made lowercase.
    websitelink = models.CharField(db_column='WebsiteLink', max_length=100, blank=True, null=True)  # Field name made lowercase.
    entrydate = models.DateTimeField(db_column='EntryDate')  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QIT_Company'


class QitDepartment(models.Model):
    transid = models.AutoField(db_column='TransID', primary_key=True)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=45)  # Field name made lowercase.
    cmptransid = models.ForeignKey(QitCompany, models.DO_NOTHING, db_column='CmpTransID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QIT_Department'


class QitNotifiicationrule(models.Model):
    n_rule_id = models.AutoField(db_column='N_Rule_ID', primary_key=True)  # Field name made lowercase.
    user_id = models.IntegerField(db_column='User_ID')  # Field name made lowercase.
    cmptransid = models.ForeignKey(QitCompany, models.DO_NOTHING, db_column='CmpTransID')  # Field name made lowercase.
    n_rule_detail = models.TextField(db_column='N_Rule_Detail', blank=True, null=True)  # Field name made lowercase.
    userrole = models.CharField(db_column='userRole', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QIT_NotifiicationRule'


class QitOtp(models.Model):
    transid = models.AutoField(db_column='TransId', primary_key=True)  # Field name made lowercase.
    e_mail = models.CharField(db_column='E_Mail', max_length=50)  # Field name made lowercase.
    verifyotp = models.IntegerField(db_column='VerifyOTP')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=2)  # Field name made lowercase.
    entrytime = models.DateTimeField(db_column='EntryTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QIT_OTP'


class QitUserlogin(models.Model):
    transid = models.AutoField(db_column='TransId', primary_key=True)  # Field name made lowercase.
    e_mail = models.CharField(db_column='E_Mail', unique=True, max_length=50)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=100)  # Field name made lowercase.
    userrole = models.CharField(db_column='UserRole', max_length=100)  # Field name made lowercase.

    @property
    def id(self):
        return self.transid

    class Meta:
        managed = False
        db_table = 'QIT_UserLogIn'


class QitUsermaster(models.Model):
    transid = models.AutoField(db_column='TransID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=100)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=100)  # Field name made lowercase.
    e_mail = models.CharField(db_column='E_Mail', unique=True, max_length=100)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cmptransid = models.ForeignKey(QitCompany, models.DO_NOTHING, db_column='CmpTransID')  # Field name made lowercase.
    cmpdeptid = models.ForeignKey(QitDepartment, models.DO_NOTHING, db_column='CmpDeptID')  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=7, null=True)  # Field name made lowercase.
    useravatar = models.TextField(db_column='UserAvatar', blank=True, null=True)  # Field name made lowercase.
    changepassstatus = models.CharField(db_column='ChangePassStatus', max_length=2,default=0)  # Field name made lowercase.
    entrydate = models.DateTimeField(db_column='EntryDate',auto_now=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)  # Field name made lowercase.
    usertype = models.CharField(db_column='UserType', max_length=45, blank=True, null=True)  # Field name made lowercase.
    createdby = models.TextField(db_column='CreatedBy', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QIT_UserMaster'


class QitVisitorinout(models.Model):
    transid = models.AutoField(db_column='TransId', primary_key=True)  # Field name made lowercase.
    vavatar = models.TextField(db_column='VAvatar',blank=True, null=True)  # Field name made lowercase.
    cnctperson = models.CharField(db_column='CnctPerson', max_length=100)  # Field name made lowercase.
    cmpdepartmentid = models.ForeignKey(QitDepartment, models.DO_NOTHING, db_column='CmpDepartmentId')  # Field name made lowercase.
    timeslot = models.DateTimeField(db_column='TimeSlot')  # Field name made lowercase.
    anyhardware = models.CharField(db_column='AnyHardware', max_length=100, blank=True, null=True)  # Field name made lowercase.
    purposeofvisit = models.CharField(db_column='PurposeOfVisit', max_length=200)  # Field name made lowercase.
    checkinstatus = models.CharField(db_column='CheckInStatus', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cmptransid = models.ForeignKey(QitCompany, models.DO_NOTHING, db_column='CmpTransId')  # Field name made lowercase.
    reason = models.CharField(db_column='Reason', max_length=200, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=2)  # Field name made lowercase.
    checkintime = models.DateTimeField(db_column='CheckInTime', blank=True, null=True)  # Field name made lowercase.
    checkouttime = models.DateTimeField(db_column='CheckOutTime', blank=True, null=True)  # Field name made lowercase.
    entrydate = models.DateTimeField(db_column='EntryDate',auto_now=True)  # Field name made lowercase.
    createdby = models.TextField(db_column='CreatedBy', blank=True, null=True)  # Field name made lowercase.
    visitortansid = models.ForeignKey('QitVisitormaster', models.DO_NOTHING, db_column='VisitorTansId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QIT_VisitorInOut'


class QitVisitormaster(models.Model):
    transid = models.AutoField(db_column='TransId', primary_key=True)  # Field name made lowercase.
    vname = models.CharField(db_column='VName', max_length=45)  # Field name made lowercase.
    phone1 = models.CharField(db_column='Phone1', unique=True, max_length=45, blank=True, null=True)  # Field name made lowercase.
    vcmpname = models.CharField(db_column='VCmpName', max_length=45)  # Field name made lowercase.
    vlocation = models.CharField(db_column='VLocation', max_length=45)  # Field name made lowercase.
    e_mail = models.CharField(db_column='E_Mail', unique=True, max_length=45)  # Field name made lowercase.
    cmptransid = models.OneToOneField(QitCompany, models.DO_NOTHING, db_column='CmpTransId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QIT_VisitorMaster'


class QitNotificationmaster(models.Model):
    transid = models.AutoField(db_column='TransId', primary_key=True)  # Field name made lowercase.
    sender_user_id = models.IntegerField(db_column='Sender_User_Id')  # Field name made lowercase.
    receiver_user_id = models.IntegerField(db_column='Receiver_User_Id')  # Field name made lowercase.
    notification_text = models.TextField(db_column='Notification_Text')  # Field name made lowercase.
    n_date_time = models.DateTimeField(db_column='N_Date_Time',auto_now=True)  # Field name made lowercase.
    chk_status = models.CharField(db_column='Chk_Status', max_length=5)  # Field name made lowercase.
    cmptransid = models.ForeignKey(QitCompany, models.DO_NOTHING, db_column='CmpTransId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QIT_NotificationMaster'