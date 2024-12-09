from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, F

from .serializers import CartItemSerializer, CategorySerializer, DistributorSerializer, FavoriteSerializer, ProductDetailSerializer, ProductSerializer, PromotionSerializer, SupplierProductsSerializer, SupplierSerializer

from .models import CartItem, Category, Distributor, Favorite, Product, ProductPrice, Promotion, Supplier

# Create your views here.
class SearchAPIView(APIView):

    def get(self, request):
        query = request.query_params.get('query')
        if not query:
            distributors = Distributor.objects.all()
            products = Product.objects.all()
        else:

            distributors = Distributor.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
            products = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
    
        distributors = DistributorSerializer(distributors, many=True)
        products = ProductSerializer(products, many=True)
            
        for item in distributors.data:
            item['type'] = 'distributor'

        for item in products.data:
            item['type'] = 'product'
        
        result = distributors.data + products.data
        return Response({
                'result': result
            })


class PromotionsListView(ListAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


class RecommendedDistributorsListView(ListAPIView):
    queryset = Distributor.objects.all().order_by('rating').values()
    serializer_class = DistributorSerializer


class CategoryListView(ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer


class SupplierBySubcategoryListView(ListAPIView):
    serializer_class = SupplierSerializer

    def get_queryset(self):
        subcategory_id = self.kwargs.get('id')
        try:
            subcategory = Category.objects.get(id=subcategory_id)
        except Category.DoesNotExist:
            return NotFound(f'Subcategory with id {subcategory_id} does not exists')
        
        return Supplier.objects.filter(category=subcategory)


class SupplierProductsListView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        supplier_id = self.kwargs.get('id')
        search_query = self.request.query_params.get('search', '')
        supplier_exists = Supplier.objects.filter(id=supplier_id).exists()
        if not supplier_exists:
            raise NotFound(f'Supplier with id {supplier_id} does not exists')
        
        products = Product.objects.filter(suppliers__supplier_id=supplier_id)

        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) | Q(sku__icontains=search_query)
            )
        return products


class AddToFavoritesCreateView(CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({
            'status': response.status_code
        })


class ProductDetailRetrieveView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer

    def get_object(self):
        product_id = self.kwargs.get('id')
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise NotFound(f'Product with id {product_id} does not exists')
        

class CartListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CartItemSerializer
        return SupplierProductsSerializer

    def get_queryset(self):
        queryset = ProductPrice.objects.filter(
            product__in=CartItem.objects.filter(user=self.request.user).values('product')
        ).annotate(
            quantity=F('product__products__quantity')
        ).values(
            'supplier__id',
            'supplier__name',
            'product__id',
            'product__name',
            'price',
            'product__image',
            'quantity'
        )

        grouped_data = {}
        for item in queryset:
            supplier_name = item['supplier__name']
            product_data = {
                "id": item['product__id'],
                "name": item['product__name'],
                "price": item['price'],
                "quantity": item['quantity'],
                "image": item['product__image']
            }

            if supplier_name not in grouped_data:
                grouped_data[supplier_name] = {
                    "id": item['supplier__id'],
                    "name": supplier_name,
                    "products": []
                }
            grouped_data[supplier_name]["products"].append(product_data)
        return list(grouped_data.values())

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Item added to cart successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
