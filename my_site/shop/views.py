from typing import Any
from django.db.models.base import Model as Model
# from django.db.models.query import QuerySet
# from django.shortcuts import render
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.views.generic import DetailView, ListView

from .models import Product, Category



class ProductDetailView(DetailView):
    "View about detail model Product"
    
    model = Product
    context_object_name = "product"
    template_name = "shop/detail-product.html"
    

class ProductListView(ListView):
    "View list products"
    
    queryset = Category.objects.all()
    template_name = "shop/list-products.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        "Add products-list"
        
        all_products = Product.objects.filter(archived=False).all()
        kwargs["products_list"] = all_products
        kwargs["show_return"] = False # Show url for return on shop:products-list
        
        return super().get_context_data(**kwargs)
    

class ProductListByCategoryView(ListView):
    "View list products by category"
    
    queryset = Category.objects.all().only("id", "name")
    template_name = "shop/list-products-by-category.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        "Add products-list and name page"
        
        search_category = self.kwargs["category"] # Take parametr `category` from url path
        all_products = Product.objects.filter(
            category=search_category,
            archived=False
        ).all() \
            .only("id", "name", "description", "price", "image")
        
        kwargs["products_list"] = all_products
        kwargs["category_title"] = Category.objects.get(pk=search_category)
        kwargs["show_return"] = True # Show url for return on shop:products-list
        
        return super().get_context_data(**kwargs)
