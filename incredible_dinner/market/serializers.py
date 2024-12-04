from rest_framework.serializers import ModelSerializer, ValidationError, IntegerField

from .models import Category, Distributor, Favorite, Product, Promotion, Supplier

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


class FavoriteSerializer(ModelSerializer):
    product_id = IntegerField(write_only=True)

    class Meta:
        model=Favorite
        fields=['product_id']
    
    def validate_product_id(self, product_id):
        if not Product.objects.filter(id=product_id).exists():
            raise ValidationError(f'Product with id {product_id} does not exists')
        return product_id

    def create(self, validated_data):
        user = self.context['request'].user
        product = Product.objects.get(id=validated_data['product_id'])

        favorite, created = Favorite.objects.get_or_create(user=user, product=product)
        if not created:
            raise ValidationError('Product is already in favorites')
        return favorite