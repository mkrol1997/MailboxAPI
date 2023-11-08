import json
import logging
import os
from datetime import date

from celery import Celery

from API.models import Mailbox, Template, Email
from API.utils import email_handler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailbox_api.settings')

app = Celery("mailbox_api")
app.config_from_object('django.conf:settings', namespace='CELERY')

logger = logging.getLogger('api_logger')


@app.task()
def send_email(json_data: json, email_id: int) -> None:
    retries = 3
    email_data = json.loads(json_data)
    mailbox = Mailbox.objects.get(id=email_data['mailbox'])
    template = Template.objects.get(id=email_data['template'])

    smtp_server = mailbox.host
    smtp_port = mailbox.port

    sender_username = mailbox.login
    sender_password = mailbox.password

    if not mailbox.is_active:
        logger.error(f'Mailbox SSL is not active. Enable SSL to use this Mailbox <id: {mailbox.id}>')
        return

    try:
        email = email_handler.fetch_email(
            sender=mailbox.email_from,
            receiver=email_data['to'],
            cc=email_data['cc'],
            bcc=email_data['bcc'],
            subject=template.subject,
            text=template.text,
        )
    except Exception as error:
        logger.error(error)
        return

    if template.attachment:
        email_handler.fetch_attachment(email, template.attachment)

    email_handler.send_smtp_tls(
        host=smtp_server,
        port=smtp_port,
        username=sender_username,
        password=sender_password,
        receiver=email_data['to'],
        email=email
    )

    Email.objects.filter(id=email_id).update(sent_date=date.today())
