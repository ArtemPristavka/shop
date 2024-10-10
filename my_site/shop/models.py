from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from typing import Any
from pathlib import Path



class Category(models.Model):
    "Model Category"
    
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs) -> None:
        "Save model with field name lower word"
        
        self.name = self.name.lower()
        return super().save(*args, **kwargs) 
    
    def __str__(self) -> str:
        "Return string object"

        return self.name
    

class Product(models.Model):
    "Model Product"
    
    name = models.CharField(max_length=80)
    description = models.TextField(max_length=600)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)
    archived = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="products",
        null=True
    )
    
    def __str__(self) -> str:
        "Return string object"
        return self.name

    def save(self, *args, **kwargs) -> None:
        "Save model with field name lower word"
        # print(self.objects.name)
        self.name = self.name.lower()
        return super().save(*args, **kwargs)
    

def generic_path_to_save_photo(instance: "ProductImage", filename: str) -> str:
    """
    Generic path to save photo in MEDIA_ROOT

    Args:
        instance (ProductImage): model ProductImage
        filename (str): name file download

    Returns:
        str: path to save file begin with MEDIA_ROOT
    """
    return f"products/product_{instance.product.pk}/{filename}"

    
class ProductImage(models.Model):
    "Model have image for product"
    
    photo = models.ImageField(
        upload_to=generic_path_to_save_photo, # type: ignore
        null=True
    )
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="image"
    )
    description = models.CharField(
        max_length=100,
        blank=True
    )
    
    def delete(self, *args, **kwargs) -> tuple[int, dict[str, int]]:
        "Delete object from DB and delete file(image) from MEDIA_ROOT"

        answer =  super().delete(*args, **kwargs)
        
        media_path: Path = settings.MEDIA_ROOT / str(self.photo)
        if media_path.exists(): # Check exists file
            media_path.unlink() # Delete Image file
            
        return answer
    
    def __str__(self) -> str:
        "Return string object"
        return f"Фото товара: {self.product.name}"


class StatusOrder(models.Model):
    "Model for status order"

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        "Return string object"
        return self.name


class Order(models.Model):
    "Model Order"

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="orders"
    )
    product = models.ManyToManyField(Product, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(     
        StatusOrder, 
        on_delete=models.SET_NULL, 
        related_name="orders",
        null=True,
        default=1 # type: ignore
    )
    
    def __str__(self) -> str:
        return f"id: {self.pk} for user: {self.user.username}"
