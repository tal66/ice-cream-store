from django.contrib import admin

from .models import *
from website.models import *

admin.site.register(IceCream)
admin.site.register(UserProfile)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'order')
