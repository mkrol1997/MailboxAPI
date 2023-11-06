from django.db import models
from django.contrib.postgres.fields import ArrayField


class Mailbox(models.Model):
    host = models.CharField(max_length=35, blank=False)
    port = models.IntegerField(default=465, blank=False)
    login = models.CharField(max_length=20, blank=False)
    password = models.CharField(max_length=20, blank=False)
    email_from = models.CharField(max_length=35, blank=False)
    use_ssl = models.BooleanField(default=True, blank=False)
    is_active = models.BooleanField(default=False)
    date = models.DateField(auto_now=True)
    last_updated = models.DateField(auto_now_add=True)

    @property
    def sent(self):
        return Email.objects.filter(mailbox=self).count()


class Template(models.Model):
    subject = models.CharField(max_length=50, blank=False)
    text = models.TextField(blank=False)
    attachment = models.FileField(blank=True)
    date = models.DateField(auto_now=True)
    last_updated = models.DateField(auto_now_add=True)


class Email(models.Model):
    mailbox = models.ForeignKey(Mailbox, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    to = ArrayField(
        base_field=models.EmailField(),
        size=None,
        blank=False,
        null=False
    )
    cc = ArrayField(
        base_field=models.EmailField(),
        size=None,
        blank=True,
        null=True
    )
    bcc = ArrayField(
        base_field=models.EmailField(),
        size=None,
        blank=True,
        null=True
    )
    reply_to = models.EmailField(default=None, blank=True, null=True)
    sent_date = models.DateField(blank=True, null=True)
    date = models.DateField(auto_now=True)
