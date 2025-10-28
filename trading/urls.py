from django.urls import path
from .views import RegisterView, AddBrokerView, SignalWebhookView, BrokerAccounts

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('brokers/', AddBrokerView.as_view(), name='add-broker'),
    path('list-brokers/', BrokerAccounts.as_view(), name='list-brokers'),
    path('webhooks/signal/', SignalWebhookView.as_view(), name='signal-webhook'),
]
