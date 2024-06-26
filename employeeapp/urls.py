from django.urls import path
from . import views

urlpatterns = [
     path('auth/jwt/create/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', views.welcome, name='welcome'),
    path('adduser/', views.adduser, name='adduser'),
    path('check_email_phone/', views.check_email_phone, name='check_email_phone'),
    path('validate_otp/', views.validate_otp, name='validate_otp'),
    path('viewprofile/', views.viewprofile, name='viewprofile'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('dashboardanalysis/', views.dashboardanalysis, name='dashboardanalysis'),
    path('categories/', views.categories, name='categories'),
    path('addsubcategories/', views.Addsubcategory.as_view()),
    path('subcategories/<int:pk>/', views.subcategories, name='subcategories'),
    path('expenses/', views.Expenses.as_view()),
    path('expenses/<int:pk>/', views.Expenses.as_view()),
    path('archive/', views.Archive.as_view()),
    path('archive/<int:pk>/', views.Archive.as_view()),
    path('subscriptiondetails/', views.Subscriptiondetails.as_view()),
    path('usersubscription/',views.UserSubscriptionView.as_view()),
    path('help/', views.Helpview.as_view()),
    path('privacypolicy/',views.Privacypolicy.as_view()),
    path('faq/',views.Faqview.as_view()),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('forgotpasswordotpvalidate/', views.forgotpasswordotpvalidate, name='forgotpasswordotpvalidate'),
    path('verify-email/', views.VerifyEmail.as_view()),
    path('VerifyOTP/', views.VerifyOTP.as_view()),
    path('Razorpaykey/', views.Razorpaykeyview.as_view()),
    path('viewreport/', views.Viewreport.as_view()),
    path('archivereport/', views.Archivereport.as_view()),
    path('subscriptionrenewal/', views.Subscriptionrenewal.as_view()),
]