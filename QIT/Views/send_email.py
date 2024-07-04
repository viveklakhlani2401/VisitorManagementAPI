from django.core.mail import EmailMultiAlternatives
from QIT.settings import EMAIL_HOST_USER



def send_html_mail(*args, **kwargs):
    subject = kwargs.get("subject")
    html_content = kwargs.get("html_content")
    recipient_list = kwargs.get("recipient_list")

    msg = EmailMultiAlternatives(subject, '', EMAIL_HOST_USER, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()