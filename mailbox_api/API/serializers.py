from rest_framework import serializers

from mailbox_drf_api.mailbox_api.API.models import Mailbox, Template, Email


class MailboxSerializer(serializers.ModelSerializer):
    sent = serializers.SerializerMethodField()

    class Meta:
        model = Mailbox
        fields = '__all__'

    def emails_sent(self, obj):
        return obj.sent


class TemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Template
        fields = '__all__'


class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Email
        fields = "__all__"
