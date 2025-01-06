from django.contrib import admin
from apps.order.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("from_date", "to_date", "is_paid")
