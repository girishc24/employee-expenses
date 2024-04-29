from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Employee(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, unique=True, null=False) 
    company = models.CharField(max_length=50,  null=True, blank=True) 
    designation = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username

class Category(models.Model):
    user = models.ForeignKey(User, related_name='categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Expense(models.Model):
    STATUS_CHOICES = [
        ('UPI', 'UPI'),
        ('Cash', 'Cash'),
        ('Credit/Dedit', 'Credit/Dedit'),
        ('Net Banking', 'Net Banking'),
    ]
    STATUS_PROFF = [
        ('TAX INVOICE', 'TAX INVOICE'),
        ('NOT APPLICABLE', 'NOT APPLICABLE'),
        ('VOUCHER ', 'VOUCHER'),
        ('RESPECTIVE BILL', 'RESPECTIVE BILL'),
    ]
    created_date = models.DateField(auto_now_add=True)
    updated_date=models.DateField(auto_now=True)
    user = models.ForeignKey(User, related_name='expenses', on_delete=models.CASCADE)
    expense_date = models.DateField(auto_now=False)
    amount = models.DecimalField( max_digits=10, decimal_places=2)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    subcategory = models.ForeignKey("Subcategory", on_delete=models.CASCADE)
    payment =  models.CharField(max_length=50,  choices=STATUS_CHOICES, default='UPI')
    note = models.CharField(max_length=500, null=True, blank=True)
    proof = models.CharField( max_length=50, choices=STATUS_PROFF, default='RESPECTIVE BILL')
    document = models.FileField(upload_to='employeeapp/images', max_length=100)
    

