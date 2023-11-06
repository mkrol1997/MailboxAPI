from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from API.models import Mailbox, Template
from API.serializers import MailboxSerializer, TemplateSerializer


class MailboxView(ListCreateAPIView):
    queryset = Mailbox.objects.all()
    serializer_class = MailboxSerializer


class MailboxDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Mailbox.objects.all()
    serializer_class = MailboxSerializer


class TemplateView(ListCreateAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer


class TemplateDetailView(ListCreateAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
