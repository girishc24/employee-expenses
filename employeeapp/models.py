from django.db import models
from django.contrib.auth.models import User 
from .validators import validate_file_size
from django.conf import settings
from urllib.parse import urljoin
from django.utils import timezone

class Employee(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, unique=True, null=False) 
    company = models.CharField(max_length=50,  null=True, blank=True) 
    designation = models.CharField(max_length=50, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    emp_id = models.CharField(max_length=50, null=True, blank=True)
    photo = models.FileField(upload_to='employeeapp/images', max_length=100,validators=[validate_file_size], null=True, blank=True)
    
    def __str__(self) -> str:
        return self.user.username

class Category(models.Model):
    user = models.ForeignKey(User, related_name='categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    photo = models.FileField(upload_to='employeeapp/images', max_length=100,validators=[validate_file_size])
    

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
        ('UPI TRANSACTIONS', 'UPI TRANSACTIONS'),
        ('RELATED BILL', 'RELATED BILL'),
        ('OTHERS', 'OTHERS'),
    ]
    created_date = models.DateField(auto_now_add=True)
    updated_date=models.DateField(auto_now=True)
    archived_date=models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, related_name='expenses', on_delete=models.CASCADE)
    expense_date = models.DateField(auto_now=False)
    amount = models.DecimalField( max_digits=10, decimal_places=2)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    subcategory = models.ForeignKey("Subcategory", on_delete=models.CASCADE)
    payment =  models.CharField(max_length=50,  choices=STATUS_CHOICES, default='UPI')
    note = models.CharField(max_length=500, null=True, blank=True)
    proof = models.CharField( max_length=50, choices=STATUS_PROOF, default='RELATED BILL')
    #document = models.FileField(upload_to='employeeapp/images', max_length=100, validators=[validate_file_size], null=True, blank=True)
    archived =models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.category.name} - {self.expense_date}"
    
class ExpenseDocument(models.Model):
    expense = models.ForeignKey(Expense, related_name='documents', on_delete=models.CASCADE)
    document = models.FileField(upload_to='employeeapp/images', max_length=1000, validators=[validate_file_size],null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Document for {self.expense.category.name} - {self.id}"

class Subscriptions(models.Model):
    DURATION_CHOICES = [
        (1, '1 Month'),
        (3, '3 Months'),
        (6, '6 Months'),
    ]
    created_date = models.DateField(auto_now_add=True)
    updated_date=models.DateField(auto_now=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.IntegerField(choices=DURATION_CHOICES)
    duration = models.IntegerField(null=False, blank=False)  
    available= models.IntegerField(null=False, blank=False)  
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

class Usersubscription(models.Model):
    created_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='subscription', on_delete=models.CASCADE)
    sub_plan = models.ForeignKey(Subscriptions, related_name='subscriptionplan', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    razorpay_order_id = models.CharField(max_length=255, unique=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, unique=True, null=True)
    amt = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100)
    available = models.IntegerField(null=False, blank=False)
    
    
    def __str__(self)-> str:
        return f"{self.user.username} - {self.sub_plan.name}"


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

class Termscondition(models.Model):
    description=models.TextField()

    def __str__(self)-> str:
        return "Terms & Condition"

class Faq(models.Model):
    date=models.DateField(auto_now_add=True)
    question=models.CharField(max_length=200, null=False, blank=False)
    answer=models.TextField()

    def __str__(self):
        return self.question
    
class Razorpaykey(models.Model):
    date=models.DateField(auto_now_add=True)
    keyid=models.CharField(max_length=200, null=False, blank=False)
    keysecret=models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return "Razorpay Key Values"
    
class DeletedAccount(models.Model):
    date=models.DateField(auto_now_add=True)
    emailid=models.CharField(max_length=100, null=False, blank=False)
    phoneno=models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return f"{self.date}-{self.emailid}-{self.phoneno}"
