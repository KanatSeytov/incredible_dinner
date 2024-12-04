from django.db import models

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
    city = models.CharField(max_length=100, default='Astana')
    delivery_time = models.CharField(max_length=100, default='Завтра')


"""- `id` (integer) – ID акции.
- `title` (string) – название акции.
- `image` (string) – URL изображения.
- `link` (string) – ссылка на акцию."""
class Promotion(models.Model):
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=255, blank=True) # rename to image_url
    link = models.CharField(max_length=255, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='children')


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    logo = models.CharField(max_length=255, null=True, blank=True) # rename to logo_url
    rating = models.FloatField(default=0)
    category = models.ForeignKey(Category, related_name='suppliers', on_delete=models.PROTECT)


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='suppliers')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')
    price = models.FloatField()
    delivery_time = models.CharField(max_length=100)
