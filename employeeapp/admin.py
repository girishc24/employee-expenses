from django.contrib import admin
from  django.contrib.auth.models  import User
from .models import Employee, Category, Subcategory

admin.site.register(Employee)
admin.site.register(Category)
admin.site.register(Subcategory)
