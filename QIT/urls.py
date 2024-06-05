"""
URL configuration for QIT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from QIT.Views import common,company_master,dept_master,user_master
from rest_framework.routers import DefaultRouter
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('VMS/GenerateOTP', common.GenerateOTP),
    path('VMS/VerifyOTP', common.VerifyOTP),
    path('VMS/Register', company_master.CreateCompany),
    path('VMS/GetComapnyData/<str:qrCode>', company_master.GetComapnyData),
    path('VMS/Login', common.login_view),
    path('VMS/CompanyData', company_master.getCompany),
    path('VMS/secure', common.secure_view),
    path('VMS/refreshToken', common.token_refresh),
    path('VMS/ForgetPasswordOTP', common.Forget_Password_Send_OTP),
    path('VMS/VerifyForgetPasswordOTP', common.VerifyForgetpasswordOTP),
    path('VMS/GenerateNewPassword', common.generate_newPassword),
    path("VMS/test", common.getWebsocketTest),
    path("VMS/Department/Save", dept_master.SaveDepartment),
    path("VMS/Department/GetByCid/<int:cid>", dept_master.GetAllDeptByCId),
    path("VMS/Department/Update", dept_master.EditDepartment),
    path("VMS/Department/Delete/<int:did>/<int:cid>", dept_master.DeleteDepartment),
    path('VMS/User/Get/<int:cmpId>', user_master.get_user),
    path('VMS/User/GetById/<int:cmpId>/<int:transid>', user_master.get_user_by_id),
    path('VMS/User/Save', user_master.save_user),
    path('VMS/User/Update/<int:cmpId>/<int:transid>', user_master.update_user),
    path('VMS/User/Delete/<int:cmpId>/<int:transid>', user_master.delete_user),
]
