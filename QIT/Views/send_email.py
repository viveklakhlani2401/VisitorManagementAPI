from django.core.mail import EmailMessage
from QIT.settings import EMAIL_HOST_USER


import threading
from threading import Thread

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMessage(self.subject, self.html_content, EMAIL_HOST_USER, self.recipient_list)
        msg.content_subtype = "html"
        msg.send()

def send_html_mail(subject, html_content, recipient_list):
    EmailThread(subject, html_content, recipient_list).start()

# from django.core.mail import EmailMessage
# from QIT.settings import EMAIL_HOST_USER
# from django.core.mail import get_connection
# import threading

# class EmailThread(threading.Thread):
#     def __init__(self, subject, html_content, recipient_list):
#         self.subject = subject
#         self.recipient_list = recipient_list
#         self.html_content = html_content
#         threading.Thread.__init__(self)

#     def run(self):
#         connection = get_connection()  # Get the default connection
#         for recipient in self.recipient_list:
#             try:
#                 msg = EmailMessage(self.subject, self.html_content, EMAIL_HOST_USER, [recipient], connection=connection)
#                 msg.content_subtype = "html"
#                 msg.send()
#                 print(f"Email sent to {recipient}")
#             except Exception as e:
#                 print(f"Failed to send email to {recipient}: {e}")

# def send_html_mail(subject, html_content, recipient_list):
#     print("come here")
#     EmailThread(subject, html_content, recipient_list).start()
