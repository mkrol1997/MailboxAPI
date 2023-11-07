from API.models import Mailbox, Template, Email
from API.serializers import MailboxSerializer, TemplateSerializer, EmailSerializer
from API.tasks import send_email

from rest_framework.renderers import JSONRenderer
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)


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

    def perform_create(self, serializer):
        obj = serializer.save()
        serialized_json = JSONRenderer().render(serializer.data)
        send_email.delay(serialized_json, obj.id)
