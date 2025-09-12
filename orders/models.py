from django.db import models
import uuid
from register.models import CustomUser
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)  # Quantity per item instance
    img = models.CharField(max_length=255, blank=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through='OrderItem')
    reference = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('pending_payment', 'Pending Payment'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed')
        ],
        default='pending_payment'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_intent_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.reference}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Quantity specific to this order

    class Meta:
        unique_together = ('order', 'item')



# Create your models here.


# class Item(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.PositiveIntegerField(default=1)
#     img = models.CharField(max_length=255, blank=True)
#     shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

#     def __str__(self):
#         return self.name

#     # @property
#     # def total_price(self):
#     #     """Calculate total price as price * quantity."""
#     #     return self.price * self.quantity

#     # @property
#     # def total_shipping_cost(self):
#     #     """Calculate total shipping cost as shipping_cost * quantity."""
#     #     return self.shipping_cost * self.quantity

#     # def __str__(self):
#     #     return f"{self.name} (x{self.quantity}) - ${self.total_price}"

#     class Meta:
#         verbose_name = "Item"
#         verbose_name_plural = "Items"
#         # unique_together = [['name', 'price']]


# class Order(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
#     items = models.ManyToManyField(Item, related_name='orders')
#     reference = models.CharField(max_length=50, null=True, blank=True, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     status = models.CharField(
#         max_length=20,
#         choices=[
#             ('pending_payment', 'Pending Payment'),
#             ('processing', 'Processing'),
#             ('completed', 'Completed'),
#             ('failed', 'Failed')
#         ],
#         default='pending_payment'
#     )
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     payment_intent_id = models.CharField(max_length=100, null=True, blank=True)

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"Order {self.reference}"
#     # class Meta:
#     #     ordering = ('-created_at',)
#     #     verbose_name = "Order"

#     def save(self, *args, **kwargs):
#         if not self.reference:
#             while True:
#                 reference = str(random.randint(10000, 99999))
#                 if not Order.objects.filter(reference=reference).exists():
#                     self.reference = reference
#                     break
#         super().save(*args, **kwargs)

#     @property
#     def total_amount(self):
#         return sum(item.total_price for item in self.items.all())

#     @property
#     def total_shipping(self):
#         return sum(item.total_shipping_cost for item in self.items.all())

#     def __str__(self):
#         return f"Order {self.reference} by {self.user.email}"
    