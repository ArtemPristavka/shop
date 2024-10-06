from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Product



class ProductDetailView(DetailView):
    "View about detail model Product"
    
    model = Product
    context_object_name = "product"
    template_name = "shop/detail-product.html"
    
    
