from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from QIT.models import QitVisitorinout,QitUsermaster 
import os
from QIT.Views.template import send_reminder
from QIT.Views.send_email import send_html_mail
@shared_task
def update_checkin_status():
    now = timezone.now()
    eight_hours_ago = now - timedelta(hours=8)
    visitors_to_update = QitVisitorinout.objects.filter(
        entrydate__lt=eight_hours_ago,
        status='A',
        checkinstatus='I'
    )
    if visitors_to_update.exists():
        visitors_to_update.update(checkinstatus='O')
    else:
        print("No visitors found matching the update criteria.")

@shared_task
def reminder_notification():
    try:
        today = timezone.now().date()
        visitors_data = QitVisitorinout.objects.filter(
            timeslot__date=today,
            status='A'
        )
        if visitors_data.exists():
            for visitors_to_remind in visitors_data:
                cmpid = visitors_to_remind.cmptransid
                statusLink = os.getenv("FRONTEND_URL") + '#/checkstatus/?cmpId=' + cmpid.qrstring
                verifyLink = os.getenv("FRONTEND_URL") +'#/Verify-Visitors'
                users = None
                users = QitUsermaster.objects.filter(username=visitors_to_remind.cnctperson,cmpdeptid=visitors_to_remind.cmpdepartmentid,cmptransid=cmpid)
                emails = []
                if users:
                    for data in users:
                        emails.append(data.e_mail)
                else:
                    users = QitUsermaster.objects.filter(cmpdeptid=visitors_to_remind.cmpdepartmentid,cmptransid=cmpid)
                    for data in users:
                        emails.append(data.e_mail)
                visitor_dict = {
                'id': visitors_to_remind.transid,
                'vName': visitors_to_remind.visitortansid.vname,
                'vPhone1':visitors_to_remind.visitortansid.phone1,
                'vCmpname': visitors_to_remind.visitortansid.vcmpname,
                'vLocation': visitors_to_remind.visitortansid.vlocation,
                'deptId': visitors_to_remind.cmpdepartmentid,
                'deptName': visitors_to_remind.cmpdepartmentid,
                'vEmail': visitors_to_remind.visitortansid.e_mail,
                'state': visitors_to_remind.checkinstatus,
                'status': visitors_to_remind.status,
                'addedBy': visitors_to_remind.createdby,
                'cnctperson': visitors_to_remind.cnctperson,
                'timeslot': visitors_to_remind.timeslot,
                'purposeofvisit': visitors_to_remind.purposeofvisit,
                'reason': visitors_to_remind.reason
            }
                message1 =  send_reminder(visitor_dict,"Visiting company reminder",statusLink,"To ensure a smooth check-in process, please click here","CheckIn")
                message2 =  send_reminder(visitor_dict,"Visitor arrival reminder",verifyLink,"To verify a visitor, please click here","verify now")
                send_html_mail(f"reminder",message2,emails)
                send_html_mail(f"reminder",message1,[visitors_to_remind.visitortansid.e_mail])
            else:
                print("No visitors found matching the update criteria.")
    except Exception as e:
        print("An error occurred: {}".format(str(e)))
