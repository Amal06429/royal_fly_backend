from django.urls import path
from .views import send_ticket_whatsapp

urlpatterns = [
    path("send-ticket/", send_ticket_whatsapp),
]
