from .views import MailboxView
from django.urls import path


urlpatterns = [
    path('mailbox/', MailboxView.as_view()),
    path('books/<int:pk>', MailboxView.as_view())
]
