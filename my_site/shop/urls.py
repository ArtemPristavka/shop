from django.urls import path

from .views import ProductDetailView, ProductListView, ProductListByCategoryView


app_name = "shop"

urlpatterns = [
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/", ProductListView.as_view(), name="products-list"),
    path(
        "products/<int:category>/", 
        ProductListByCategoryView.as_view(), 
        name="products-list-by-category"
    ),
]