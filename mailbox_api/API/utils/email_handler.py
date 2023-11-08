import logging
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.db.models import FileField

RETRIES = 3

logger = logging.getLogger('api_logger')


def fetch_email(sender, receiver, cc, bcc, subject, text) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = ', '.join(receiver)
    msg["Cc"] = ', '.join(cc)
    msg['Bcc'] = ', '.join(bcc)
    msg["Subject"] = subject
    msg.attach(MIMEText(text, "plain"))

    return msg


def fetch_attachment(email: MIMEMultipart, file: FileField) -> None:
    with file.open("rb") as attachment:
        part = MIMEApplication(attachment.read(), Name=file.name)
        part['Content-Disposition'] = f'attachment; filename="{file.name}"'
        email.attach(part)


def send_smtp_tls(host: str, port: int, username: str, password: str, receiver: str, email: MIMEMultipart) -> None:
    for attempt in range(RETRIES):
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            try:
                server.login(username, password)
                server.sendmail(username, receiver, email.as_string())
            except Exception as error:
                logger.error(error)
            else:
                return
