from rest_framework import serializers
from .models import Customer, Order, Payment
from decimal import Decimal


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'balance', 'created_at']
        read_only_fields = ['id', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'amount', 'status',
            'transaction_id', 'created_at'
        ]
        read_only_fields = ['id', 'transaction_id', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'customer_name', 'total_amount',
            'status', 'description', 'payment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, attrs):

        if self.context['request'].method == 'POST':
            attrs.pop('status')
        
        return attrs


class CreateOrderSerializer(serializers.Serializer):

    customer_id = serializers.IntegerField()
    total_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal('0.01')
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True
    )

    def validate_total_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Summa musbat bo'lishi kerak!")
        return value


class PaymentSerializer(serializers.ModelSerializer):

    customer = CustomerSerializer()

    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "amount",
            "customer",
            "order"
        )