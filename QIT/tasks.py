from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from QIT.models import QitVisitorinout,QitUsermaster,QitCompany
import os
from QIT.Views.template import send_reminder,send_reminder_user
from QIT.Views.send_email import send_html_mail
from datetime import datetime

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
            # status='A'
        )
        print("-------->10",visitors_data)
        if visitors_data.exists():
            for visitors_to_remind in visitors_data:
                cmpid = visitors_to_remind.cmptransid
                companyEntry = visitors_to_remind.cmptransid
                print("Company Enrtyt: ",companyEntry)
                print("visitors_to_remind.status: ",visitors_to_remind.status)
                # companyEntry = QitCompany.objects.filter(transid=cmpid).first()
                statusLink = os.getenv("FRONTEND_URL") + '#/checkstatus/?cmpId=' + companyEntry.qrstring
                checkLink = os.getenv("FRONTEND_URL") + '#/CheckIn/?cmpId=' + companyEntry.qrstring
                verifyLink = os.getenv("FRONTEND_URL") +'#/Verify-Visitors'
                
                users = None
                users = QitUsermaster.objects.filter(username=visitors_to_remind.cnctperson,cmpdeptid=visitors_to_remind.cmpdepartmentid,cmptransid=cmpid)
                print("-------->1")
                emails = []
                if users:
                    for data in users:
                        emails.append(data.e_mail)
                else:
                    users = QitUsermaster.objects.filter(cmpdeptid=visitors_to_remind.cmpdepartmentid,cmptransid=cmpid)
                    for data in users:
                        emails.append(data.e_mail)
                print("-------->2",emails)
                
                timestamp = visitors_to_remind.timeslot
                iso_format_str = timestamp.isoformat()
                dt = datetime.fromisoformat(iso_format_str.replace("Z", "+00:00"))
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
                    'timeslot': iso_format_str,
                    'purposeofvisit': visitors_to_remind.purposeofvisit,
                    'reason': visitors_to_remind.reason
                }
                if visitors_to_remind.status == "A":
                    message1 = send_reminder(
                        visitor_dict,
                        f"This is a friendly reminder of your upcoming visit to {companyEntry.bname}. Here are the details of your scheduled visit:",
                        companyEntry.e_mail,
                        companyEntry.bname,
                        f"<p>Next Steps:</p><p>Check-In Instructions: Upon arrival, please scan the QR code or please click the following link to check in: <a href={checkLink} class='button'>Check In</a></p>",
                        f"If you have any questions or need further information, please feel free to contact us at {companyEntry.e_mail}.",
                        "We look forward to your visit!"
                    )
                    subject = f"Reminder: Your Upcoming Visit to {companyEntry.bname}"
                    send_html_mail(subject, message1,[visitors_to_remind.visitortansid.e_mail])
                    
                    message2 =  send_reminder_user(visitor_dict,f"This is a reminder that you have a scheduled visitor coming to meet you on {dt.strftime('%d %B %Y')} at {dt.strftime('%I:%M %p')}. Here are the details:",companyEntry.e_mail,companyEntry.bname,"The visitor has been informed and will receive instructions to check in using the QR code provided.",f"Thank you for your cooperation.")
                    send_html_mail(f"Reminder: Visitor Arrival",message2,emails)
                if visitors_to_remind.status == "P":
                    print("-------->2",emails)
                    print("-------->visitors_to_remind.status",visitors_to_remind.status)
                    message2 =  send_reminder_user(visitor_dict,f"A visitor has registered to meet you at {companyEntry.bname} Your approval is required to confirm the visit. Please review the details below and provide your approval at your earliest convenience.",companyEntry.e_mail,companyEntry.bname,"Upon your approval, the visitor will be notified to enter the premises. Thank you for your prompt attention to this matter.",f"To verify and approve the visitor, please click the following link: <a href={verifyLink} class='button'>Check Status</a>")
                    send_html_mail(f"Reminder: Visitor Registration",message2,emails)
            # else:
            #     print("No visitors found matching the update criteria.")
    except Exception as e:
        print("An error occurred: {}".format(str(e)))
