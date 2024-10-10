from django.urls import path

from .views import (
    ProductDetailView, ProductListView, ProductListByCategoryView,
    AddProductByUserView, BasketUserView, DeleteProductByUserView,
    OrderView, CreateOrderView
)



app_name = "shop"

urlpatterns = [
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/", ProductListView.as_view(), name="products-list"),
    path(
        "products/<int:category>/", 
        ProductListByCategoryView.as_view(), 
        name="products-list-by-category"
    ),
    path("products/basket/", BasketUserView.as_view(), name="basket-user"),
    path("product/basket/add/<int:pk>/", AddProductByUserView.as_view(), name="add-product"),
    path(
        "products/basket/remove/<int:pk>", 
        DeleteProductByUserView.as_view(), 
        name="remove-product"
    ),
    path("products/orders/", OrderView.as_view(), name="orders-list"),
    path("products/oredrs/create/", CreateOrderView.as_view(), name="create-order"),
    
]