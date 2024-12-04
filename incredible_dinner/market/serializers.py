from rest_framework.serializers import ModelSerializer

from .models import Distributor, Product, Promotion

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
        fields=["__all__"]