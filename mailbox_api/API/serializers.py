from API.models import Mailbox, Template, Email
from rest_framework import serializers


class MailboxSerializer(serializers.ModelSerializer):
    sent = serializers.SerializerMethodField()
    password = serializers.SerializerMethodField()

    class Meta:
        model = Mailbox
        fields = '__all__'

    def get_sent(self, obj):
        return obj.sent

    def get_password(self, obj):
        return '*' * len(obj.password)


class TemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Template
        fields = '__all__'


class EmailSerializer(serializers.ModelSerializer):
    sent_date = serializers.DateField(read_only=True)

    class Meta:
        model = Email
        fields = "__all__"

