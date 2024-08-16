from django.db import models

from django.contrib.auth.models import User

from apps.common.models import BaseModel
from apps.product.models import Product


STATUS = (
    (0, 'New'),
    (1, 'Completed'),
    (2, 'Canceled'),
)


class Order(BaseModel):
    status = models.IntegerField(choices=STATUS, default=0, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="orders")
    phone = models.CharField(max_length=225, null=True, blank=True)
    full_name = models.CharField(max_length=225, null=True, blank=True)
    notes = models.CharField(max_length=225, null=True, blank=True)

    @property
    def total(self):
        return sum([item.total for item in self.items.all()])

    def __str__(self) -> str:
        return f'{self.user.username} - {self.status}'


class Cart(BaseModel):
    is_completed = models.BooleanField(default=False, null=True, blank=True)
    session_id = models.CharField(max_length=225, null=True, blank=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self) -> str:
        return self.session_id

    @property
    def total(self):
        if self.cart_items.count() == 0:
            return 0
        return sum([item.total for item in self.cart_items.all()])

    @property
    def main_total(self):
        if self.cart_items.count() == 0:
            return 0
        return sum([item.main_total for item in self.cart_items.all()])

    @property
    def items_count(self):
        if not self.cart_items:
            return 0
        return self.cart_items.count()


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items', null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)

    @property
    def total(self):
        return self.product.discount * self.quantity

    @property
    def main_total(self):
        return self.product.price * self.quantity

    def __str__(self) -> str:
        return f'{self.product.name}'


class WishList(BaseModel):
    session_id = models.CharField(max_length=225, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.product.name
