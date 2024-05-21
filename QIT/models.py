from django.db import models

class OTP(models.Model):

    TransId = models.AutoField(primary_key=True)
    E_Mail = models.EmailField(max_length=100)
    VerifyOTP = models.IntegerField(max_length=6)
    Status = models.CharField(max_length=1,default="N")
    EntryTime = models.DateTimeField(auto_now_add=True)

class Company_Master(models.Model):
    TransId = models.AutoField(primary_key=True)
    E_Mail = models.EmailField(max_length=100)
    Password = models.CharField(max_length=500)
    BusinessName = models.CharField(max_length=200)
    BUsinessLocation = models.CharField(max_length=500)

   

