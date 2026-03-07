from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Order, Customer, Payment
from .serializers import (
    CreateOrderSerializer, OrderSerializer, CustomerSerializer,
    PaymentSerializer
)
from .services import (
    OrderService,
    InsufficientBalanceError,
    OrderNotFoundError,
    InvalidOrderStatusError
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
import logging

logger = logging.getLogger(__name__)


@extend_schema(tags=['orders'])
class OrderViewSet(ModelViewSet):

    authentication_classes = ()
    permission_classes = ()
    queryset = Order.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):

        queryset = super().get_queryset()

        if self.action == "list":
            customer_id = self.request.query_params.get("customer_id")
            queryset = queryset.filter(customer_id=customer_id)
        
        return queryset

    def get_serializer_class(self):
        
        if self.action == "create":
            return CreateOrderSerializer
        return OrderSerializer
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='customer_id',
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.INT,
                required=True
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data

        try:

            order = OrderService.create_and_process_order(
                customer_id=data['customer_id'],
                total_amount=data['total_amount'],
                description=data.get('description', '')
            )

            return Response(
                {
                    "success": True,
                    "data": OrderSerializer(order).data
                },
                status=status.HTTP_201_CREATED
            )

        except OrderNotFoundError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

        except InsufficientBalanceError as err:
            return Response(
                {"success": False, "message": str(err)},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as err:
            logger.error(f"Kutilmagan xato: {str(err)}", exc_info=True)
            return Response(
                {
                    "success": False,
                    "error": str(err)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def retrieve(self, request, pk=None):
        
        order = get_object_or_404(
            Order.objects.select_related('customer', 'payment'),
            id=pk
        )

        return Response(
            {
                "success": True,
                "data": OrderSerializer(order).data
            }
        )
    
    @action(detail=True, methods=['PATCH'], url_path='confirm')
    def confirm_order(self, request, pk=None):

        order = self.get_object()

        order.status = "completed"

        order.save(update_fields=['status', 'updated_at'])

        return Response({
            "message": "Order completed"
        })
    
    @action(detail=True, methods=['POST'], url_path='cancel')
    def cancel_order(self, request, pk=None):

        try:
            order = OrderService.cancel_order(pk)
            return Response(
                {
                    "success": True,
                    "message": f"Buyurtma bekor qilindi. {order.total_amount} so'm qaytarildi.",
                    "data": OrderSerializer(order).data
                }
            )

        except OrderNotFoundError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

        except InvalidOrderStatusError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(tags=['customers'])
class CustomerViewSet(ModelViewSet):

    authentication_classes = ()
    permission_classes = ()
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')


class PaymentListView(ListAPIView):

    authentication_classes = ()
    permission_classes = ()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        customer_id = self.request.query_params.get('customer_id')

        return Payment.objects \
            .filter(customer__isnull=False, customer_id=customer_id) \
            .select_related('customer', 'order')
    
    @extend_schema(
        tags=['payments'],
        parameters=[
            OpenApiParameter(
                name='customer_id',
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.INT,
                required=True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)