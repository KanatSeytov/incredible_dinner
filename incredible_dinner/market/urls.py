
from django.urls import path

from .views import CategoryAPIView, PromotionsListAPIView, RecommendedDistributorsListApiView, SearchAPIView

urlpatterns = [
    path('search/', SearchAPIView.as_view()),
    path('carousel/promotions/', PromotionsListAPIView.as_view()),
    path('carousel/recommended-distributors/', RecommendedDistributorsListApiView.as_view()),
    path('categories/', CategoryAPIView.as_view())
]
