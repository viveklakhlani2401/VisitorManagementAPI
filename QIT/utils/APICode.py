from enum import Enum
class APICodeClass(Enum):
    Notification_Add = 1001
    Notification_Get = 1002
    Notification_Read = 1003

    Department_Add = 2001
    Department_Get = 2002
    Department_Edit = 2003
    Department_Delete = 2004

    Notification_Rule_Save = 3001
    Notification_Rule_Get = 3002
    Notification_Rule_Preset = 3003

    Auth_Rule_Save = 4001
    Auth_Rule_Get = 4002
    Auth_Rule_Preset = 4003

    User_Save = 5001
    User_Get = 5002
    User_Edit = 5003
    User_Delete = 5004
    User_GetById = 5005
    User_Profile_Edit = 5006

    Company_Save = 6001
    # Company_Get = 600
    Company_Edit = 6003
    Company_GetByQR = 6004
    Company_GetByCId = 6005

    Visitor_Save = 7001     
    Visitor_Get = 7002
    Visitor_Edit = 7003
    Visitor_Verify = 7004
    Visitor_GetById = 7005
    Visitor_ChkOutByCmp = 7006

    Visitor_Mobile_Save = 7101
    Visitor_Mobile_ChkStatus = 7102
    Visitor_Mobile_GetByEmail = 7103
    Visitor_Mobile_ChkOutByV = 7104

    Auth_Generate_OTP = 8001
    Auth_Verify_OTP = 8002
    Auth_LogIn = 8003
    Auth_ForgetPWD_Cmp = 8004
    Auth_GenerateNewPWD_Cmp = 8005
    Auth_VerifyForgetPWD_OTP = 8006
    Auth_ForgetPWD_User = 8007
    Auth_RefreshToken = 8008

