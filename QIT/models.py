# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class QitCompanymaster(models.Model):
    transid = models.AutoField(db_column='TransId', primary_key=True)  # Field name made lowercase.
    e_mail = models.CharField(db_column='E_Mail', unique=True, max_length=50)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=100)  # Field name made lowercase.
    businessname = models.CharField(db_column='BusinessName', max_length=200)  # Field name made lowercase.
    businesslocation = models.CharField(db_column='BusinessLocation', max_length=500)  # Field name made lowercase.
    qrcodeid = models.CharField(db_column='QRCodeId', max_length=100)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=2)  # Field name made lowercase.
    entrydate = models.DateTimeField(db_column='EntryDate',auto_now=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QIT_CompanyMaster'


class QitOtp(models.Model):
    transid = models.AutoField(db_column='TransId', primary_key=True)  # Field name made lowercase.
    e_mail = models.CharField(db_column='E_Mail', max_length=50)  # Field name made lowercase.
    verifyotp = models.IntegerField(db_column='VerifyOTP')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=2)  # Field name made lowercase.
    entrytime = models.DateTimeField(db_column='EntryTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QIT_OTP'
