import json
import logging
import os
import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Celery

from .models import Mailbox, Template, Email

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

    msg = MIMEMultipart()
    msg["From"] = mailbox.email_from
    msg["To"] = ', '.join(data['to'])
    msg["Cc"] = ', '.join(data['cc'])
    msg['Bcc'] = ', '.join(data['bcc'])
    msg["Subject"] = template.subject
    msg.attach(MIMEText(template.text, "plain"))

    while retries > 0:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            try:
                server.login(sender_username, sender_password)
                server.sendmail(sender_username, sender_username, msg.as_string())
            except Exception as e:
                retries -= 1
                logger.error(e)
            else:
                Email.objects.filter(id=email_id).update(sent_date=date.today())
                return
