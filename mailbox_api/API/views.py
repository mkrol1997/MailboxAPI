from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from API.models import Mailbox, Template, Email
from API.serializers import MailboxSerializer, TemplateSerializer, EmailSerializer


class MailboxView(ListCreateAPIView):
    queryset = Mailbox.objects.all()
    serializer_class = MailboxSerializer


class MailboxDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Mailbox.objects.all()
    serializer_class = MailboxSerializer


class TemplateView(ListCreateAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer


class TemplateDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer


class EmailView(ListCreateAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer