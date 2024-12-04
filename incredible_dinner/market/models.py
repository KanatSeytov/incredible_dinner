from django.db import models

"""- `type` (string) – тип результата (`product` или `distributor`).
- `id` (integer) – ID элемента.
- `name` (string) – название.
- `description` (string) – краткое описание.
- `image` (string) – URL изображения."""

# Create your models here.
class Distributor(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    image = models.CharField(max_length=255)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
