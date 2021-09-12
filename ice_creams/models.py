from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

DEFAULT_PRICE = 6


class IceCream(models.Model):
    name = models.CharField(max_length=20, unique=True, default="my ice cream")
    description = models.CharField(max_length=100)
    ingredients = models.CharField(max_length=140)
    allergy_info = models.CharField(max_length=80, blank=True)
    pic_url = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, default="user")
    price_usd = models.IntegerField(default=DEFAULT_PRICE)

    def __str__(self):
        return f"{self.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(IceCream)

    def __str__(self):
        return f"{self.user.username}"


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order:{self.id}, date:{self.order_date.date()}"

    def get_total_price(self):
        total = 0
        for item in self.orderitem_set.all():
            total += item.get_total_price()
        return total


class OrderItem(models.Model):
    item = models.ForeignKey(IceCream, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    unit_price_usd = models.IntegerField()

    def get_total_price(self):
        return self.unit_price_usd * self.quantity
