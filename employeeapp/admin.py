from django.contrib import admin
from  django.contrib.auth.models  import User
from .models import *

admin.site.register(Employee)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Usersubscription)
admin.site.register(Subscriptions)
admin.site.register(Help)
admin.site.register(PrivacyPolicy)
admin.site.register(Termscondition)
admin.site.register(Faq)
admin.site.register(Expense)
#admin.site.register(ExpenseDocument)
admin.site.register(Razorpaykey)
admin.site.register(ExpenseDocument)
admin.site.register(DeletedAccount)
