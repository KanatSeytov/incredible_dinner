from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.serializers import ValidationError
from django.db.models import Q

from .serializers import CategorySerializer, DistributorSerializer, FavoriteSerializer, ProductSerializer, PromotionSerializer, SupplierSerializer

from .models import Category, Distributor, Favorite, Product, Promotion, Supplier

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

class PromotionsListAPIView(ListAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


class RecommendedDistributorsListApiView(ListAPIView):
    queryset = Distributor.objects.all().order_by('rating').values()
    serializer_class = DistributorSerializer


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer


class SupplierBySubcategoryListAPIView(ListAPIView):
    serializer_class = SupplierSerializer

    def get_queryset(self):
        subcategory_id = self.kwargs.get('id')
        try:
            subcategory = Category.objects.get(id=subcategory_id)
        except Category.DoesNotExist:
            return NotFound(f'Subcategory with id {subcategory_id} does not exists')
        
        return Supplier.objects.filter(category=subcategory)
        # return super().get_queryset()
    
class SupplierProductsListAPIView(ListAPIView):
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
    
class AddToFavoritesCreateAPIView(CreateAPIView):
    serializer_class = FavoriteSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'status': '201'}, status=status.HTTP_201_CREATED, headers=headers)
            # return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({
                'status': str(e.detail)
            }, status=status.HTTP_400_BAD_REQUEST)
         
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
    