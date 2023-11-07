import json
import smtplib
import ssl
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from .models import Mailbox, Template, Email
from celery import Celery
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailbox_api.settings')

app = Celery("mailbox_api")
app.config_from_object('django.conf:settings', namespace='CELERY')

logger = logging.getLogger('api_logger')


@app.task()
def send_email(json_data, email_id):
    retries = 3

    data = json.loads(json_data)
    mailbox = Mailbox.objects.get(id=data['mailbox'])
    template = Template.objects.get(id=data['template'])

    if not mailbox.is_active:
        logger.error(f'Mailbox SSL is not active. Enable SSL to use this Mailbox <id: {mailbox.id}>')
        return

    smtp_server = mailbox.host
    smtp_port = mailbox.port

    sender_username = mailbox.login
    sender_password = mailbox.password

    mail_to = ', '.join(data['to'])
    mail_cc = ', '.join(data['cc'])
    mail_bcc = ', '.join(data['bcc'])

    msg = MIMEMultipart()
    msg["From"] = mailbox.email_from
    msg["To"] = mail_to
    msg["Cc"] = mail_cc
    msg['Bcc'] = mail_bcc
    msg["Subject"] = template.subject
    msg.attach(MIMEText(template.text, "plain"))

    while retries > 0:
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_username, sender_password)
                server.sendmail(sender_username, sender_username, msg.as_string())
        except Exception as e:
            retries -= 1
            logger.error(e)
        else:
            from datetime import date

            Email.objects.filter(id=email_id).update(sent_date=date.today())
            return


"""
{
    "to": ["emailziutka1@gmail.com", "test@email.com"],
    "cc": ["test@email.com", "test@email.com"],
    "bcc": ["test@email.com", "test@email.com"],
    "reply_to": "test@email.com",
    "mailbox": 1,
    "template": 1
}
"""