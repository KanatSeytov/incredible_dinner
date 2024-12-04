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


"""- `id` (integer) – ID акции.
- `title` (string) – название акции.
- `image` (string) – URL изображения.
- `link` (string) – ссылка на акцию."""
class Promotion(models.Model):
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=255) # rename to image_url
    link = models.CharField(max_length=255)

