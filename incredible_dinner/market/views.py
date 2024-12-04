from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.db.models import Q

from .serializers import DistributorSerializer, ProductSerializer, PromotionSerializer

from .models import Distributor, Product, Promotion

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