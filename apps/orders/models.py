# models.py

from django.db import models
from decimal import Decimal
from django.utils.translation import gettext_lazy as _
import uuid


class Customer(models.Model):

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customers'
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return f"{self.name} ({self.phone}) — Balans: {self.balance}"

    def has_sufficient_balance(self, amount: Decimal) -> bool:
        return self.balance >= amount


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = 'pending', 'Kutilmoqda'
        PAID = 'paid', 'To\'langan'
        COMPLETED = 'completed', 'Bajarildi'
        CANCELLED = 'cancelled', 'Bekor qilindi'

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders',
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        verbose_name = _('Order')
        verbose_name_plural = ('Orders')
        ordering = ('-created_at',)

    def __str__(self):
        return f"Buyurtma #{self.id} | {self.customer.name} | {self.status}"

    @property
    def can_be_cancelled(self) -> bool:
        return self.status in [self.Status.PENDING, self.Status.PAID]


class Payment(models.Model):

    class PaymentStatus(models.TextChoices):
        SUCCESS = 'success', 'Muvaffaqiyatli'
        FAILED = 'failed', 'Muvaffaqiyatsiz'
        REFUNDED = 'refunded', 'Qaytarildi'
    
    customer = models.ForeignKey(
        Customer,
        related_name='payments',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.SUCCESS
    )

    transaction_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        ordering = ('-created_at',)

    def __str__(self):
        return f"To'lov #{self.transaction_id} | {self.order} | {self.status}"