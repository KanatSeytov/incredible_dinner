from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .serializers import CartItemSerializer, CategorySerializer, DistributorSerializer, FavoriteSerializer, ProductDetailSerializer, ProductSerializer, PromotionSerializer, SupplierSerializer

from .models import CartItem, Category, Distributor, Favorite, Product, Promotion, Supplier

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
        # return super().get_queryset()
    
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


class AddToCartCreateView(CreateAPIView):
    serializer_class = CartItemSerializer
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