from rest_framework.serializers import ModelSerializer

from .models import Category, Distributor, Product, Promotion, Supplier

class DistributorSerializer(ModelSerializer):
    class Meta:
        model=Distributor
        fields="__all__"
    

class ProductSerializer(ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"

class PromotionSerializer(ModelSerializer):
    class Meta:
        model=Promotion
        fields="__all__"
    

class SubcategorySerializer(ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'
    

class CategorySerializer(ModelSerializer):
    subcategories = SubcategorySerializer(many=True, source='children')

    class Meta:
        model=Category
        fields=['id', 'name', 'subcategories']


class SupplierSerializer(ModelSerializer):
    class Meta:
        model=Supplier
        fields='__all__'