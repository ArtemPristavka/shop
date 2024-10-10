from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet

from .models import Category, Product, ProductImage, StatusOrder, Order



admin.site.disable_action("delete_selected")


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
    list_display = ["id", "name", "price", "archived"]
    list_display_links = ["id", "name"]
    readonly_fields = ["id", "created_at"]
    search_fields = ["name__icontains", "description__icontains"]
    search_help_text = "Поиск по Имени и Описанию продукта"
    
    inlines = [ProductImageInline]
    
    actions = ["make_archived_products", "make_unarchiving_products"]
    
    @admin.action(description="Archiving products")
    def make_archived_products(self, request: HttpRequest, queryset: QuerySet) -> None:
        "Archiving products"
        
        updated = queryset.update(archived=True)
        self.message_user(
            request=request,
            message=f"Successfull maked archived products in cout: {updated}"
        )
        
    @admin.action(description="Unarchinig products")
    def make_unarchiving_products(self, request: HttpRequest, queryset: QuerySet) -> None:
        "Unarchiving products"
        
        updated = queryset.update(archived=False)
        self.message_user(
            request=request,
            message=f"Successfull maked unarchived products in cout: {updated}"
        )


@admin.register(StatusOrder)
class StatusOrderAdmin(admin.ModelAdmin):
    
    fields = ["id", "name"]
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    search_fields = ["name__icontains"]
    search_helt_text = "Поиск по названию статуса"
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    
    fields = ["id", "user", "product", "status", "created_at"]
    list_display = ["id", "user", "status", "created_at"]
    list_display_links = ["id", "user", "status", "created_at"]
    readonly_fields = ["id", "created_at"]
    
