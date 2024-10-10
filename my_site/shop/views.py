from typing import Any, List
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import RedirectView
from django.urls import reverse, reverse_lazy

from .models import Product, Category, Order



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
        "Add in context to products-list"
        
        all_products = Product.objects.filter(archived=False).all()
        kwargs["products_list"] = all_products
        kwargs["show_return"] = False # Show url for return on shop:products-list
        
        return super().get_context_data(**kwargs)
    

class ProductListByCategoryView(ListView):
    "View list products by category"
    
    queryset = Category.objects.all().only("id", "name")
    template_name = "shop/list-products-by-category.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        "Add in context to products-list and name page"
        
        search_category = self.kwargs["category"] # Take parametr `category` from url path
        all_products = Product.objects.filter( # Seach product by category
            category=search_category,
            archived=False
        ).all() \
            .only("id", "name", "description", "price", "image")
        
        kwargs["products_list"] = all_products
        kwargs["category_title"] = Category.objects.get(pk=search_category)
        kwargs["show_return"] = True # Show url for return on shop:products-list
        
        return super().get_context_data(**kwargs)
    

class AddProductByUserView(RedirectView):
    "View for add products in session(basket) and redirect shop -> product-detail"
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        "Get id(pk) product and add her in session (basket) = List[int]"

        if request.user.is_authenticated:
            if kwargs.get("pk"): # Get id(pk) product
                if request.session.get("basket"):
                    request.session["basket"].append(kwargs.get("pk")) # Add id(pk) in session(basket)
                    request.session.save() # Save session last update
                else:
                    request.session["basket"] = [kwargs.get("pk")] # Add id(pk) in session(basket)
                    request.session.save() # Save session last updated
                    
        return super().get(request, *args, **kwargs)
    
    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        "Redirect on shop -> product-detail by id(pk) product"
        
        product_id = kwargs.get("pk") # Get id(pk) product
        if self.request.user.is_authenticated:
            return reverse("shop:product-detail", kwargs={"pk": product_id})
        
        return reverse("my_auth:register-user")
    

class DeleteProductByUserView(RedirectView):
    "View for delete product from session(basket) and redirect shop -> basket-user"
    
    url = reverse_lazy("shop:basket-user")
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        "Delete product from session(basket) by id(pk)"

        if request.user.is_authenticated:
            if kwargs.get("pk"): 
                basket: List[int] = request.session["basket"] # Get session(basket)
                basket.pop(basket.index(kwargs["pk"]))  # Delete product from session(basket)
                request.session.save() # Save session last updated
                
        return super().get(request, *args, **kwargs)


class BasketUserView(TemplateView):
    "View for basket-user"
    
    template_name = "shop/basket.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        "Get product from DB by id(pk) have is session(basket)"

        # Get session(basket)
        basket_products = self.request.session.get("basket")
        if basket_products:
            need_products = Product.objects.filter( # Search product
                pk__in=basket_products              # by id(pk)
            ).only("id", "name", "price")
            
            kwargs["products"] = need_products # Add in context
            
        return super().get_context_data(**kwargs)


class OrderView(ListView):
    "View for show orders user"
    
    template_name = "shop/orders.html"
    
    def get_queryset(self) -> QuerySet[Any]:
        user_id = self.request.user.pk
        return Order.objects.filter(user=user_id).select_related("status")
        # TODO Add in template status

class CreateOrderView(RedirectView):
    "View for create order and redivrect on shop -> orders-list"

    url = reverse_lazy("shop:orders-list")
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        "Create order and clear session(basket)"
        
        all_products = request.session.get("basket") # Get pk products from session(basket)
        if all_products:
            order = Order.objects.create(
                user=request.user
            )
            for i_pk in all_products: # Add products by order
                order.product.add(Product.objects.get(pk=i_pk))
            else:
                order.save() # Save order
                del request.session["basket"] # Delete basket from session
                request.session.save() # Save session last delete basket

        return super().post(request, *args, **kwargs)
