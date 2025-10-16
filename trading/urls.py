from django.urls import path
from .views import RegisterView, AddBrokerView, SignalWebhookView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('brokers/', AddBrokerView.as_view(), name='add-broker'),
    path('webhooks/signal/', SignalWebhookView.as_view(), name='signal-webhook'),
]
