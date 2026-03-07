from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.orders.views import OrderViewSet, CustomerViewSet, PaymentListView


router = DefaultRouter()
router.register('orders', OrderViewSet, basename='orders')
router.register('customers', CustomerViewSet, basename='customers')

urlpatterns = [
    path('', include(router.urls)),
    path('payments/', PaymentListView.as_view(), name='payments')
]