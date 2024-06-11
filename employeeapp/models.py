from django.db import models
from django.contrib.auth.models import User
from .validators import validate_file_size
from django.conf import settings
from urllib.parse import urljoin

class Employee(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, unique=True, null=False) 
    company = models.CharField(max_length=50,  null=True, blank=True) 
    designation = models.CharField(max_length=50, null=True, blank=True)
    photo = models.FileField(upload_to='employeeapp/images', max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username

class Category(models.Model):
    user = models.ForeignKey(User, related_name='categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(User, related_name='subcategories', on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}, {self.category}'


class Expense(models.Model):
    STATUS_CHOICES = [
        ('UPI', 'UPI'),
        ('Cash', 'Cash'),
        ('Credit/Debit', 'Credit/Debit'),
        ('Net Banking', 'Net Banking'),
    ]
    STATUS_PROOF = [
        ('TAX INVOICE', 'TAX INVOICE'),
        ('NOT APPLICABLE', 'NOT APPLICABLE'),
        ('VOUCHER', 'VOUCHER'),
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
    proof = models.CharField( max_length=50, choices=STATUS_PROOF, default='RESPECTIVE BILL')
    document = models.FileField(upload_to='employeeapp/images', max_length=100, validators=[validate_file_size])
    archived =models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.category.name
    
    def get_document_url(self):
        if self.document:
            return urljoin(settings.MEDIA_URL, self.document.url)
        return None

class Subscriptions(models.Model):
    created_date = models.DateField(auto_now_add=True)
    updated_date=models.DateField(auto_now=True)
    duration = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self) -> str:
        return self.duration

class Usersubscription(models.Model):
    user = models.ForeignKey(User, related_name='subscription', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    
    def __str__(self)-> str:
        return self.user.username


class Help(models.Model):
    email=models.EmailField(max_length=200)
    phone=models.CharField(max_length=50, unique=True, null=False) 
    description=models.TextField()

    def __str__(self) -> str:
        return self.email

class PrivacyPolicy(models.Model):
    description=models.TextField()

    def __str__(self)-> str:
        return "Privacy Policy"

class Faq(models.Model):
    date=models.DateField(auto_now_add=True)
    question=models.CharField(max_length=200, null=False, blank=False)
    answer=models.TextField()

    def __str__(self):
        return self.question
    