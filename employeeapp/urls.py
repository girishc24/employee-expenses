from django.urls import path
from . import views

urlpatterns = [
    path('auth/jwt/create/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/jwt/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('', views.home, name='home'),
    path('privacy/', views.privacy, name='privacypolicy'),
    path('termsandcondition/', views.termsandcondition, name='termsandcondition'),
    path('refundpolicy/', views.refundpolicy, name='refundpolicy'),
    path('api/adduser/', views.adduser, name='adduser'),
    path('api/check_email_phone/', views.check_email_phone, name='check_email_phone'),
    path('api/validate_otp/', views.validate_otp, name='validate_otp'),
    path('api/viewprofile/', views.viewprofile, name='viewprofile'),
    path('api/editprofile/', views.editprofile, name='editprofile'),
    path('api/dashboardanalysis/', views.dashboardanalysis, name='dashboardanalysis'),
    path('api/categories/', views.categories, name='categories'),
    path('api/addsubcategories/<int:pk>/', views.Addsubcategory.as_view()),
    path('api/subcategories/<int:pk>/', views.subcategories, name='subcategories'),
    path('api/expenses/', views.Expenses.as_view()),
    path('api/expenses/<int:pk>/', views.Expenses.as_view()),
    path('api/archive/', views.Archive.as_view()),
    path('api/archive/<int:pk>/', views.Archive.as_view()),
    path('api/subscriptiondetails/', views.Subscriptiondetails.as_view()),
    path('api/usersubscription/',views.UserSubscriptionView.as_view()),
    path('api/help/', views.Helpview.as_view()),
    path('api/privacypolicy/',views.Privacypolicy.as_view()),
    path('api/termsandcondition/',views.Termsandcondition.as_view()),
    path('api/faq/',views.Faqview.as_view()),
    path('api/forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('api/forgotpasswordotpvalidate/', views.forgotpasswordotpvalidate, name='forgotpasswordotpvalidate'),
    path('api/verify-email/', views.VerifyEmail.as_view()),
    path('api/VerifyOTP/', views.VerifyOTP.as_view()),
    path('api/Razorpaykey/', views.Razorpaykeyview.as_view()),
    path('api/viewreport/', views.Viewreport.as_view()),
    path('api/archivereport/', views.Archivereport.as_view()),
    path('api/subscriptionrenewal/', views.Subscriptionrenewal.as_view()),
    path('api/resetdata/', views.Resetdata.as_view()),
]
