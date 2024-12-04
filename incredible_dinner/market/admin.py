from django.contrib import admin

from .models import Category, Distributor, Product

# Register your models here.
admin.site.register(Distributor)
admin.site.register(Product)
admin.site.register(Category)
