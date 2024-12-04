from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.db.models import Q

from .serializers import CategorySerializer, DistributorSerializer, ProductSerializer, PromotionSerializer, SupplierSerializer

from .models import Category, Distributor, Product, Promotion, Supplier

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
                "result": result
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
            return NotFound(f'Subcategory with id {subcategory_id} not found')
        
        return Supplier.objects.filter(category=subcategory)
        # return super().get_queryset()