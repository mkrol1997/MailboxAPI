from .views import MailboxView, MailboxDetailView, TemplateView, TemplateDetailView, EmailView
from django.urls import path


urlpatterns = [
    path('mailbox/', MailboxView.as_view()),
    path('mailbox/<int:pk>', MailboxDetailView.as_view()),
    path('template/', TemplateView.as_view()),
    path('template/<int:pk>', TemplateDetailView.as_view()),
    path('email/', EmailView.as_view()),
]
