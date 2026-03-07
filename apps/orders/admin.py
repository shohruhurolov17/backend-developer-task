from django.contrib import admin
from apps.orders.models import Customer, Order, Payment


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'phone'
    )
    search_fields = ('id',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'status',
        'total_amount'
    )
    search_fields = ('id',)
    autocomplete_fields = ('customer', )
    # fields = ('')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'status',
        'amount'
    )

    autocomplete_fields = ('order',)