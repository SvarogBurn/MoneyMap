from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    """Model za kategorije troškova."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"

class Transaction(models.Model):
    date = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    
    class Meta:
        abstract = True

class Income(Transaction):
    """Model za income."""

    def __str__(self):
        return f"{self.name} - {self.user.username}"


class Expense(Transaction):
    """Model svih troškova."""
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    is_fixed = models.BooleanField(default=True)
    is_necessity = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
    
class Goal(models.Model):
    """Model za ciljeve štednje"""
    name = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    saved = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.user.username}"