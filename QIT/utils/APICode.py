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
    Auth_ForgetPWD_OTP_Cmp = 8004
    Auth_GenerateNewPWD_Cmp = 8005
    Auth_VerifyForgetPWD_OTP = 8006
    Auth_ForgetPWD_User = 8007
    Auth_RefreshToken = 8008


class APICodeMessages:
    messages = {
        APICodeClass.Notification_Add: "Error in adding notification.",
        APICodeClass.Notification_Get: "Error in getting notification.",
        APICodeClass.Notification_Read: "Error in reading notification.",
        
        APICodeClass.Department_Add: "Error in adding department.",
        APICodeClass.Department_Get: "Error in getting department.",
        APICodeClass.Department_Edit: "Error in editing department.",
        APICodeClass.Department_Delete: "Error in deleting department.",
        
        APICodeClass.Notification_Rule_Save: "Error in saving notification rule.",
        APICodeClass.Notification_Rule_Get: "Error in getting notification rule.",
        APICodeClass.Notification_Rule_Preset: "Error in presetting notification rule.",
        
        APICodeClass.Auth_Rule_Save: "Error in saving authorization rule.",
        APICodeClass.Auth_Rule_Get: "Error in getting authorization rule.",
        APICodeClass.Auth_Rule_Preset: "Error in presetting authorization rule.",
        
        APICodeClass.User_Save: "Error in saving user.",
        APICodeClass.User_Get: "Error in getting user.",
        APICodeClass.User_Edit: "Error in editing user.",
        APICodeClass.User_Delete: "Error in deleting user.",
        APICodeClass.User_GetById: "Error in getting user by ID.",
        APICodeClass.User_Profile_Edit: "Error in editing user profile.",
        
        APICodeClass.Company_Save: "Error in saving company.",
        # APICodeClass.Company_Get: "Error in getting company.",
        APICodeClass.Company_Edit: "Error in editing company.",
        APICodeClass.Company_GetByQR: "Error in getting company by QR code.",
        APICodeClass.Company_GetByCId: "Error in getting company by ID.",
        
        APICodeClass.Visitor_Save: "Error in saving visitor.",
        APICodeClass.Visitor_Get: "Error in getting visitor.",
        APICodeClass.Visitor_Edit: "Error in editing visitor.",
        APICodeClass.Visitor_Verify: "Error in verifying visitor.",
        APICodeClass.Visitor_GetById: "Error in getting visitor by ID.",
        APICodeClass.Visitor_ChkOutByCmp: "Error in checking out visitor by company.",
        
        APICodeClass.Visitor_Mobile_Save: "Error in saving mobile visitor.",
        APICodeClass.Visitor_Mobile_ChkStatus: "Error in checking mobile visitor status.",
        APICodeClass.Visitor_Mobile_GetByEmail: "Error in getting mobile visitor by email.",
        APICodeClass.Visitor_Mobile_ChkOutByV: "Error in checking out mobile visitor.",
        
        APICodeClass.Auth_Generate_OTP: "Error in generating OTP.",
        APICodeClass.Auth_Verify_OTP: "Error in verifying OTP.",
        APICodeClass.Auth_LogIn: "Error in logging in.",
        APICodeClass.Auth_ForgetPWD_OTP_Cmp: "Error in company password recovery.",
        APICodeClass.Auth_GenerateNewPWD_Cmp: "Error in generating new company password.",
        APICodeClass.Auth_VerifyForgetPWD_OTP: "Error in verifying OTP for password recovery.",
        APICodeClass.Auth_ForgetPWD_User: "Error in user password recovery.",
        APICodeClass.Auth_RefreshToken: "Error in refreshing token."
    }
    
    @staticmethod
    def get_message(code):
        return APICodeMessages.messages.get(code, "Unknown error code.")
