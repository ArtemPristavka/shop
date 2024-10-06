from typing import Iterable
from django.db import models


class Category(models.Model):
    "Model Category"
    
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs) -> None:
        "Save model with lower word"
        
        self.name = self.name.lower()
        return super().save(*args, **kwargs) 
    

class Product(models.Model):
    "Model Product"
    
    name = models.CharField(max_length=80)
    description = models.TextField(max_length=600)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)
    archived = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        "Save model with lower word"
        
        self.name = self.name.lower()
        return super().save(*args, **kwargs)
    