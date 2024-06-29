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
from QIT.Views import common,company_master,dept_master,user_master,authorization_master,visitor_master,notification_master,reports,log
from rest_framework.routers import DefaultRouter
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('VMS/GenerateOTP', common.GenerateOTP),
    path('VMS/VerifyOTP', common.VerifyOTP),
    path('VMS/Register', company_master.CreateCompany),
    path('VMS/GetComapnyData/<str:qrCode>', company_master.GetComapnyData),
    path('VMS/GetComapnyDataById/<int:cid>', company_master.GetComapnyDataById),
    path('VMS/Company/Edit', company_master.EditComapnyDataById),
    path('VMS/Login', common.login_view),
    path('VMS/CompanyData', company_master.getCompany),
    path('VMS/secure', common.secure_view),
    path('VMS/refreshToken', common.token_refresh),
    path('VMS/ForgetPasswordOTP', common.Forget_Password_Send_OTP),
    path('VMS/ForgetPwdVerifyOTP', common.ForgetpwdVerifyOTP),
    path('VMS/ForgetPasswordRequest', common.changeUserPWDReq),
    path('VMS/GenerateNewPassword', common.generate_newPassword),
    path("VMS/test", common.getWebsocketTest),
    path("VMS/Department/Save", dept_master.SaveDepartment),
    path("VMS/Department/GetByCid/<int:cid>", dept_master.GetAllDeptByCId),
    path("VMS/Department/Update", dept_master.EditDepartment),
    path("VMS/Department/Delete/<int:did>/<int:cid>", dept_master.DeleteDepartment),
    path('VMS/User/Get/<str:status>/<int:cmpId>', user_master.get_user),
    path('VMS/User/GetById/<int:cmpId>/<int:transid>', user_master.get_user_by_id),
    path('VMS/User/Save', user_master.save_user),
    path('VMS/User/Delete/<int:cmpId>/<int:transid>', user_master.delete_user),
    path('VMS/User/Update', user_master.update_user),
    path('VMS/User/UpdateProfile', user_master.update_user_profile),
    # path('VMS/User/GenerateOTP', user_master.Company_User_GenerateOTP),
    path('VMS/AuthUser/Save', authorization_master.SaveAuthRule),
    path('VMS/AuthUser/Preset', authorization_master.AuthenticationPreSetRule),
    path('VMS/AuthUser/GET', authorization_master.GetAuthRule),
    path('VMS/NotificationAuthUser/Save', notification_master.SaveNotificationRule),
    path('VMS/NotificationAuthUser/Preset', notification_master.NotificationPreSetRule),
    path('VMS/NotificationAuthUser/GET', notification_master.GetNotificationRule),
    path('VMS/Notification/Save', notification_master.SaveNotification),
    path('VMS/Notification/GET', notification_master.GetNotification),
    path('VMS/Notification/Read', notification_master.ReadNotification),
    # path('VMS/Visitor/GenerateOTP', visitor_master.Visitor_GenerateOTP),
    path('VMS/Visitor/Save', visitor_master.Save_Visitor),
    path('VMS/Visitor/GetByEmail', visitor_master.GetVisitorByE_Mail),
    path('VMS/Visitor/GetAll/<str:status>/<int:cid>', visitor_master.GetAllVisitor),
    path('VMS/Visitor/GetVisitorDetail/<int:vid>/<int:cid>', visitor_master.GetVisitorDetail),
    path('VMS/Visitor/VerifyVisitor', visitor_master.verifyVisitor),
    path('VMS/Visitor/CheckStatus', visitor_master.chkStatus),
    path('VMS/Visitor/CheckOut', visitor_master.checkoutVisitor),
    path('VMS/Visitor/Edit', visitor_master.EditVerifyVisitor),
    path('VMS/Report/VisitorReport', reports.GetVisitorReport),
    path('VMS/SaveAPILog', log.save_log),
    path('VMS/GetAPILog', log.Get_log),
]
