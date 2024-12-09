from rest_framework.serializers import ModelSerializer, ValidationError, IntegerField, SerializerMethodField, CharField, DecimalField, FloatField, Serializer

from .models import CartItem, Category, Distributor, Favorite, Product, ProductPrice, Promotion, Supplier

class DistributorSerializer(ModelSerializer):
    class Meta:
        model=Distributor
        fields=['id', 'name', 'description', 'image']
    

class ProductSerializer(ModelSerializer):
    class Meta:
        model=Product
        fields=['id', 'name', 'description', 'image'] 

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
    
    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise ValidationError(f'Product with id {value} does not exists')
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        product = Product.objects.get(id=validated_data['product_id'])

        favorite, created = Favorite.objects.get_or_create(user=user, product=product)
        if not created:
            raise ValidationError('Product is already in favorites')
        return favorite


class UpdateCartSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class AddToCartSerializer(ModelSerializer):
    product_id = IntegerField(write_only=True)
    quantity = IntegerField(write_only=True, min_value=1)

    class Meta:
        model=CartItem
        fields=['product_id', 'quantity']
        

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise ValidationError(f'Product with id {value} does not exists')
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        product = Product.objects.get(id=validated_data['product_id'])
        quantity = validated_data['quantity']

        cart_item, created = CartItem.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity = quantity
            cart_item.save()
        return cart_item


class ProductDetailSerializer(ModelSerializer):
    price = SerializerMethodField()
    characteristics = SerializerMethodField()
    suppliers = SerializerMethodField()

    class Meta:
        model=Product
        fields='__all__'

    def get_price(self, obj):
        return {
            'retail': obj.price_retail,
            'wholesale': obj.price_wholesale
        }
    
    def get_characteristics(self, obj):
        return [{'name': key, 'value': value} for key, value in obj.characteristics.items()]
    
    def get_suppliers(self, obj):
        supplier_prices = ProductPrice.objects.filter(product=obj)
        return [
            {
                'id': sp.supplier.id,
                'name': sp.supplier.name, 
                'price': sp.price,
                'delivery_time': sp.delivery_time
            }
            for sp in supplier_prices
        ]
    
class CartProductSerializer(Serializer):
    id = IntegerField()
    name = CharField(max_length=100)
    price = DecimalField(max_digits=10, decimal_places=2)
    image = CharField(max_length=255)
    quantity = IntegerField()


class SupplierProductsSerializer(Serializer):
    id = IntegerField()
    name = CharField()
    products = CartProductSerializer(many=True)
