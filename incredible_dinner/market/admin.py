from django.contrib import admin

from .models import Distributor, Product

# Register your models here.
admin.site.register(Distributor)
admin.site.register(Product)