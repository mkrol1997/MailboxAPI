from rest_framework.generics import (
    ListCreateAPIView,
)

from API.models import Mailbox
from API.serializers import MailboxSerializer


class MailboxView(ListCreateAPIView):
    queryset = Mailbox.objects.all()
    serializer_class = MailboxSerializer
