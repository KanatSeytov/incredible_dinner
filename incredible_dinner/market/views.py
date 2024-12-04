from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from .serializers import DistributorSerializer, ProductSerializer

from .models import Distributor, Product

# Create your views here.
class SearchAPIView(APIView):

    def get(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response({
                "error": "no data found"
            })

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