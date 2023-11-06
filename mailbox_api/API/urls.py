from .views import MailboxView, MailboxDetailView, TemplateView, TemplateDetailView
from django.urls import path


urlpatterns = [
    path('mailbox/', MailboxView.as_view()),
    path('mailbox/<int:pk>', MailboxDetailView.as_view()),
    path('template/', TemplateView.as_view()),
    path('template/<int:pk>', TemplateDetailView.as_view()),
]
