from .views import MailboxView, MailboxDetailView
from django.urls import path


urlpatterns = [
    path('mailbox/', MailboxView.as_view()),
    path('mailbox/<int:pk>', MailboxDetailView.as_view())
]
