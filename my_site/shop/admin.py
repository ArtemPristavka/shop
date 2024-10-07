from django.contrib import admin

from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    "Model Category for Admin site"
    
    fields = ["id", "name", "created_at"]
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    readonly_fields = ["id", "created_at"]
    search_fields = ["name__icontains"]
    search_help_text = "Поиск по Имени категории"


class ProductImageInline(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    "Model Product for Admin site"
    
    fields = ["id", "category", "name", "description", "price", "created_at", "archived"]
    list_display = ["id", "name", "price"]
    list_display_links = ["id", "name"]
    readonly_fields = ["id", "created_at"]
    search_fields = ["name__icontains", "description__icontains"]
    search_help_text = "Поиск по Имени и Описанию продукта"
    
    inlines = [
        ProductImageInline
    ]
    