from django.contrib import admin

from .models import CartItem, Category, Distributor, Favorite, Product, ProductPrice, Supplier

# Register your models here.
admin.site.register(Distributor)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(ProductPrice)
admin.site.register(Favorite)
admin.site.register(CartItem)