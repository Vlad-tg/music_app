from celery import shared_task
from django.conf import settings
from django.template.loader import get_template
from .models import *
from django.core.mail import EmailMultiAlternatives


@shared_task
def send_mail_task():
    print("Mail sending.......")
    subject = 'welcome to Celery world'
    html_template = get_template('/music_app/core/templates/core/advertising/ad_for_send.html')
    send_html = html_template.render()
    message = 'Hi thanks you for standing with us'
    email_from = 'MusicStore <{}>'.format(settings.EMAIL_HOST_USER)
    users = Customer.objects.all()
    customer_send_advertising = Customer.objects.filter(send_advertising=True)
    for u in users:
        if u.send_advertising == True:
            recipient_list = [u.user.email, ]
            sm = EmailMultiAlternatives(subject, message, email_from, recipient_list)
            sm.attach_alternative(send_html, "text/html")
            sm.send()
    return "Mail has been sent........"


