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
