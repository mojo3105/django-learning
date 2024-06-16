from django.db import models
from django.utils import timezone
from sqlalchemy import null

# Create your models here.
class SalesMan(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(null=False)
    phone_no = models.BigIntegerField(default=0)
    address = models.CharField(max_length=1000, default=null)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Name:{self.name}, Email:{self.email}, Phone No.:{self.phone_no}"
    
class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price_in_dollars = models.DecimalField(null=False, default=10.0, max_digits=10, decimal_places=2)
    agent = models.ForeignKey(SalesMan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Name:{self.name}, Price:{self.price_in_dollars}"