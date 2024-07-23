from django.db import models
from django.db.models.functions import Now
from django.core.validators import (MinValueValidator, MaxValueValidator)

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveSmallIntegerField()
    # image = models.ImageField()
    description = models.TextField(max_length=400)
    stock = models.PositiveIntegerField()
    archived = models.BooleanField(default=False)
    discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    product_category = models.ForeignKey("ProductCategory", on_delete=models.RESTRICT)
    
    def fprice(self):
        cents = int(self.price) / 100
        return f"{cents:.2f}".replace(".", ",")

    def __str__(self):
        return f"{self.name}"
    
class ProductCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"
    
class Order(models.Model):
    payment_type = models.ForeignKey("PaymentType", on_delete=models.RESTRICT)
    shipping_tax = models.ForeignKey("ShippingTax", on_delete=models.RESTRICT, null=True)
    shipping_tax_name = models.CharField(max_length=50, null=True)
    shipping_tax_value = models.PositiveSmallIntegerField(null=True)
    created = models.DateTimeField(db_default=Now())
    
    def __str__(self):
        return f"Order: {self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.RESTRICT)
    order_status = models.ForeignKey("OrderStatus", on_delete=models.RESTRICT, default=1)
    product = models.ForeignKey("Product", on_delete=models.RESTRICT)
    product_price = models.PositiveSmallIntegerField()
    product_discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    quantity = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return f"Order item: {self.id}"
    
class OrderStatus(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.name}"

class PaymentType(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"{self.name}"

class ShippingTax(models.Model):
    name = models.CharField(max_length=50)
    value = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return f"{self.name}"
    