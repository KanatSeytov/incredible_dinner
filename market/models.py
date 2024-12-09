from django.db import models
from django.contrib.auth.models import User
"""- `type` (string) – тип результата (`product` или `distributor`).
- `id` (integer) – ID элемента.
- `name` (string) – название.
- `description` (string) – краткое описание.
- `image` (string) – URL изображения."""


class Distributor(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True)
    logo = models.CharField(max_length=255, null=True, blank=True) # rename to logo_url
    rating = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"{self.name}"

"""- `id` (integer) – ID товара.
- `sku` (string) – артикул.
- `name` (string) – название.
- `city` (string) – город.
- `image` (string) – URL изображения.
- `delivery_time` (string) – срок доставки."""
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True)
    sku = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    delivery_time = models.CharField(max_length=100)
    price_retail = models.DecimalField(max_digits=10, decimal_places=2)
    price_wholesale = models.DecimalField(max_digits=10, decimal_places=2)
    min_order = models.PositiveIntegerField()
    characteristics = models.JSONField()

    def __str__(self) -> str:
        return f"{self.name}"
    

class Promotion(models.Model):
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=255, blank=True) # rename to image_url
    link = models.CharField(max_length=255, blank=True)
    
    def __str__(self) -> str:
        return f"{self.title}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='children')
    
    def __str__(self) -> str:
        return f"{self.name}"


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    logo = models.CharField(max_length=255, null=True, blank=True) # rename to logo_url
    rating = models.FloatField(default=0)
    category = models.ForeignKey(Category, related_name='suppliers', on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.name}"


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='suppliers')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')
    price = models.FloatField()
    delivery_time = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.product}, {self.supplier}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together= ('user', 'product')
    
    def __str__(self) -> str:
        return f"{self.user}, {self.product}"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self) -> str:
        return f"{self.user}, {self.product}, {self.quantity}"