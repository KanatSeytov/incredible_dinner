
from django.urls import path

from .views import AddToCartView, AddToFavoritesView, CategoryView, ProductDetailView, PromotionsView, RecommendedDistributorsView, SearchView, SupplierBySubcategoryView, SupplierProductsView

urlpatterns = [
    path('search/', SearchView.as_view()),
    path('carousel/promotions/', PromotionsView.as_view()),
    path('carousel/recommended-distributors/', RecommendedDistributorsView.as_view()),
    path('categories/', CategoryView.as_view()),
    path('subcategory/<int:id>/suppliers/', SupplierBySubcategoryView.as_view(), name='suppliers-by-category'),
    path('supplier/<int:id>/products/', SupplierProductsView.as_view(), name='supplier-products'),
    path('favorites/', AddToFavoritesView.as_view(), name='add-to-favorites'),
    path('cart/', AddToCartView.as_view(), name='add-to-favorites'),
    path('product/<int:id>/', ProductDetailView.as_view(), name='add-to-favorites'),
]
