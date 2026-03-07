from django.urls import path, include
from apps.common.views import CurrencyConvertAPIView, FileProcessingTaskViewSet, PaymentWebhookView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('tasks', FileProcessingTaskViewSet, basename='tasks')


urlpatterns = [
    path('', include(router.urls)),
    path('currency/convert/', CurrencyConvertAPIView.as_view(), name='currency_convert'),
    path('webhooks/payment/', PaymentWebhookView.as_view(), name='payment_webhook')
]