from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('adduser/', views.adduser, name='adduser'),
    path('viewprofile/', views.viewprofile, name='viewprofile'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('categories/', views.categories, name='categories'),
    path('subcategories/<int:pk>/', views.subcategories, name='subcategories'),
    path('expenses/', views.Expenses.as_view()),
    
]