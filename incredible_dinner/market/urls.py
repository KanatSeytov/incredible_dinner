
from django.urls import path

from .views import PromotionsListAPIView, SearchAPIView

urlpatterns = [
    path('search/', SearchAPIView.as_view()),
    path('carousel/promotions/', PromotionsListAPIView.as_view()),
    # path('/carousel/recommended-distributors', )
]
