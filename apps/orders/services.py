from django.db import transaction
from django.utils import timezone
from decimal import Decimal
from .models import Customer, Order, Payment
import logging

logger = logging.getLogger(__name__)


class InsufficientBalanceError(Exception):
    """Balans yetarli emas"""
    pass


class OrderNotFoundError(Exception):
    """Buyurtma topilmadi"""
    pass


class InvalidOrderStatusError(Exception):
    """Buyurtma holati noto'g'ri"""
    pass


class OrderService:

    @staticmethod
    @transaction.atomic
    def create_and_process_order(
        customer_id: int,
        total_amount: Decimal,
        description: str = ""
    ) -> Order:

        logger.info(f"Buyurtma yaratish boshlandi: mijoz={customer_id}, summa={total_amount}")

        try:
            customer = Customer.objects.select_for_update().get(
                id=customer_id
            )
        except Customer.DoesNotExist:
            raise OrderNotFoundError(f"Mijoz topilmadi yoki faol emas: ID={customer_id}")

        if not customer.has_sufficient_balance(total_amount):
            raise InsufficientBalanceError(
                f"Balans yetarli emas! "
                f"Kerak: {total_amount}, Mavjud: {customer.balance}"
            )

        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount,
            status=Order.Status.PENDING,
            description=description
        )

        logger.info(f"Buyurtma yaratildi: #{order.id}")

        customer.balance -= total_amount
        customer.save(update_fields=['balance', 'updated_at'])
        logger.info(f"Balansdan ayirildi: {total_amount}. Yangi balans: {customer.balance}")

        payment = Payment.objects.create(
            order=order,
            amount=total_amount,
            status=Payment.PaymentStatus.SUCCESS,
            customer=customer
        )
        logger.info(f"To'lov saqlandi: tranzaksiya={payment.transaction_id}")

        order.status = Order.Status.PAID
        order.save(update_fields=['status', 'updated_at'])
        logger.info(f"Buyurtma uchun to'lov qilindi: #{order.id}")

        return order

    @staticmethod
    @transaction.atomic
    def cancel_order(order_id: int) -> Order:

        try:
            order = Order.objects.select_for_update().get(id=order_id)
        except Order.DoesNotExist:
            raise OrderNotFoundError(f"Buyurtma topilmadi: ID={order_id}")

        if not order.can_be_cancelled:
            raise InvalidOrderStatusError(
                f"Buyurtma bekor qilib bo'lmaydi. Hozirgi holat: {order.status}"
            )

        customer = Customer.objects.select_for_update().get(id=order.customer_id)

        customer.balance += order.total_amount
        customer.save(update_fields=['balance', 'updated_at'])

        if hasattr(order, 'payment'):
            order.payment.status = Payment.PaymentStatus.REFUNDED
            order.payment.save(update_fields=['status', 'updated_at'])

        order.status = Order.Status.CANCELLED
        order.save(update_fields=['status', 'updated_at'])

        logger.info(f"Buyurtma bekor qilindi: #{order_id}, pul qaytarildi: {order.total_amount}")
        return order