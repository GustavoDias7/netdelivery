from django.db import models
from django.core.validators import (MinValueValidator, MaxValueValidator)

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
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
    