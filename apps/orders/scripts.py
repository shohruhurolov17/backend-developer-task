from apps.orders.models import Order
from django.db.models.functions import TruncMonth
from django.db.models import OuterRef, Count, Exists, Avg, Min, F


def customer_monthly_stats() -> list[dict]:

    monthly_stats = (
        Order.objects \
            .filter(status="completed") \
            .annotate(month=TruncMonth("created_at")) \
            .values("month", "customer_id") \
            .annotate(
                total_orders=Count("id"),
                avg_check=Avg('total_amount'),
                first_order=Min('created_at')
            ) \
        .order_by('month', 'customer_id')
    )

    return list(monthly_stats)


def monthly_stats() -> list[dict]:

    previous_orders = Order.objects.filter(
        customer=OuterRef('customer_id'),
        created_at__lt=OuterRef('created_at')
    )

    monthly_stats = (
        Order.objects
        .filter(status="completed") \
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(
            total_orders=Count('id'),
            total_customers=Count('customer', distinct=True),
            returning_customers=Count(
                'customer',
                filter=Exists(previous_orders),
                distinct=True
            )
        )
        .annotate(
            returning_customer_ratio=F('returning_customers') * 100.0 / F('total_customers')
        )
        .order_by('month')
    )

    return list(monthly_stats)

