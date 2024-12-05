
from django.urls import path

from .views import (SearchAPIView, PromotionsListView, 
                    RecommendedDistributorsListView, CategoryListView, 
                    SupplierBySubcategoryListView, SupplierProductsListView, 
                    AddToFavoritesCreateView, AddToCartCreateView, 
                    ProductDetailRetrieveView)

urlpatterns = [
    path('search/', SearchAPIView.as_view()),
    path('carousel/promotions/', PromotionsListView.as_view()),
    path('carousel/recommended-distributors/', RecommendedDistributorsListView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('subcategory/<int:id>/suppliers/', SupplierBySubcategoryListView.as_view(), name='suppliers-by-category'),
    path('supplier/<int:id>/products/', SupplierProductsListView.as_view(), name='supplier-products'),
    path('favorites/', AddToFavoritesCreateView.as_view(), name='add-to-favorites'),
    path('cart/', AddToCartCreateView.as_view(), name='add-to-favorites'),
    path('product/<int:id>/', ProductDetailRetrieveView.as_view(), name='add-to-favorites'),
    # path('cart/', CartView.as_view())
]
