
from django.urls import path

from .views import CategoryListAPIView, PromotionsListAPIView, RecommendedDistributorsListApiView, SearchAPIView, SupplierBySubcategoryListAPIView, SupplierProductsListAPIView

urlpatterns = [
    path('search/', SearchAPIView.as_view()),
    path('carousel/promotions/', PromotionsListAPIView.as_view()),
    path('carousel/recommended-distributors/', RecommendedDistributorsListApiView.as_view()),
    path('categories/', CategoryListAPIView.as_view()),
    path('subcategory/<int:id>/suppliers/', SupplierBySubcategoryListAPIView.as_view(), name='suppliers-by-category'),
    path('supplier/<int:id>/products/', SupplierProductsListAPIView.as_view(), name='supplier-products')
]
