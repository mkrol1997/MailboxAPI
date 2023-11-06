from API.models import Mailbox, Template, Email
from rest_framework import serializers


class MailboxSerializer(serializers.ModelSerializer):
    sent = serializers.SerializerMethodField()

    class Meta:
        model = Mailbox
        fields = '__all__'

    def get_sent(self, obj):
        return obj.sent


class TemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Template
        fields = '__all__'


class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Email
        fields = "__all__"
