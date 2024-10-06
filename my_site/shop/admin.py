from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    "Model Category for Admin site"
    
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    "Model Product for Admin site"
    
    pass
