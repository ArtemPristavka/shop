from typing import Iterable
from django.db import models



class Category(models.Model):
    "Model Category"
    
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs) -> None:
        "Save model with field name lower word"
        
        self.name = self.name.lower()
        return super().save(*args, **kwargs) 
    

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
        return self.name

    def save(self, *args, **kwargs) -> None:
        "Save model with field name lower word"
        
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
    
    def __str__(self) -> str:
        return f"Фото товара: {self.product.name}"
    