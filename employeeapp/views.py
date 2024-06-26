from datetime import date
import random
import string
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response  import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from . serializers import UserCreateSerializer, EmployeeSerializers, UserSerializer, UserAddSerializersnew, CategorySerializer, SubcategorySerializer, ExpenseSerializer, SubscriptionSerialixer, HelpSerializer, PrivacyPolicySerializer, FaqSerializer, UsersubscriptionSerializer, ExpenseSerializerNew, ExpenseSerializerEdit, ExpenseSerializerview, AddsubcategorySerializer, UserEditSerializersnew,EmployeeEditSerializers,RazorpaykeySerializer
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.contrib.auth.hashers import make_password
from .models import Employee,Category, Subcategory,  Expense, Subscriptions, Usersubscription, Help, PrivacyPolicy,Faq, Razorpaykey
from django.utils.dateparse import parse_date
import pandas as pd
from openpyxl import Workbook
from io import BytesIO
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['access_expiry'] = refresh.access_token.payload['exp']
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


def welcome(request):
    return  HttpResponse("Welcome")

@api_view(['POST'])
def adduser(request):
    if request.method == 'POST':
        user_serializer = UserCreateSerializer(data=request.data)
        employee_serializers = EmployeeSerializers(data=request.data)

        if user_serializer.is_valid(raise_exception=True) and employee_serializers.is_valid(raise_exception=True):
            user = user_serializer.save()
            employee = employee_serializers.save(user=user)
            response_data = {
                'user': user_serializer.data,
                'employee': employee_serializers.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response({'error': user_serializer.errors, 'employee_error': employee_serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response({'error': 'GET Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        def add_months(d, months):
            new_month = d.month + months
            year_offset = (new_month - 1) // 12
            new_month = (new_month - 1) % 12 + 1
            new_year = d.year + year_offset
            new_day = min(d.day, [31,
                                29 if new_year % 4 == 0 and (new_year % 100 != 0 or new_year % 400 == 0) else 28,
                                31, 30, 31, 30, 31, 31, 30, 31, 30, 31][new_month - 1])
            return date(new_year, new_month, new_day)
        today = date.today()
        three_months_later = add_months(today, 3)
        plan = Subscriptions.objects.get(id=1)
        print(f"Plan ID {plan}")
        subscription = Usersubscription.objects.create(
            user=instance,
            sub_plan=plan,  
            start_date=today,
            end_date=three_months_later,
            amt=plan.price,
            status='Completed'
        )
        print(f"Created subscription: {subscription}")
        # Create default categories
        travel_category = Category.objects.create(name='Travel', user=instance)
        accomodation_category = Category.objects.create(name='Accommodation', user=instance)
        food_category = Category.objects.create(name='Food Expenses', user=instance)
        items_category = Category.objects.create(name='Items Purchased', user=instance)
        miscellaneous_category = Category.objects.create(name='Miscellaneous', user=instance)

        # Create subcategories for 'Travel'
        Subcategory.objects.create(category=travel_category, name='Flight', user=instance)
        Subcategory.objects.create(category=travel_category, name='Taxi', user=instance)
        Subcategory.objects.create(category=travel_category, name='Bus', user=instance)
        Subcategory.objects.create(category=travel_category, name='Train', user=instance)
        Subcategory.objects.create(category=travel_category, name='Rapido', user=instance)
        Subcategory.objects.create(category=travel_category, name='Ola', user=instance)
        Subcategory.objects.create(category=travel_category, name='Uber', user=instance)
        Subcategory.objects.create(category=travel_category, name='Namma Yatri', user=instance)
        Subcategory.objects.create(category=travel_category, name='Others', user=instance)

        # Create subcategories for 'Travel'
        Subcategory.objects.create(category=accomodation_category, name='Accommodation', user=instance)

        # Create subcategories for 'Items Purchased'
        Subcategory.objects.create(category=items_category, name='Items Purchased', user=instance)

        # Create subcategories for 'Food Expenses'
        Subcategory.objects.create(category=food_category, name='Breakfast', user=instance)
        Subcategory.objects.create(category=food_category, name='Lunch', user=instance)
        Subcategory.objects.create(category=food_category, name='Snacks', user=instance)
        Subcategory.objects.create(category=food_category, name='Dinner', user=instance)

        # Create subcategories for 'Miscellaneous'
        Subcategory.objects.create(category=miscellaneous_category, name='Medical Expenses', user=instance)
        Subcategory.objects.create(category=miscellaneous_category, name='Cell phone', user=instance)
        Subcategory.objects.create(category=miscellaneous_category, name='Health & Wellness', user=instance)
        Subcategory.objects.create(category=miscellaneous_category, name='Learning & Development', user=instance)
        Subcategory.objects.create(category=miscellaneous_category, name='Entertainment / Refreshment', user=instance)

@api_view(['POST'])
def check_email_phone(request):
    if request.method == 'POST':
        email = request.data.get('email', None)
        phone = request.data.get('phone', None)
        
        if email and phone:
            if User.objects.filter(email=email).exists():
                return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            elif Employee.objects.filter(phone=phone).exists():
                return Response({'message': 'Phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                otp = ''.join(random.choices(string.digits, k=6))
                send_mail(
                    'OTP Verification',
                    f'Your OTP is: {otp}',
                    'Email Verification',
                    [email],
                    fail_silently=False,
                )
                return Response({'message': 'OTP sent to your email', 'OTP': otp}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Both email and phone must be provided'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def validate_otp(request):
    if request.method == 'POST':
        otp_entered = request.data.get('otp_entered')
        otp_generated = request.data.get('otp_generated')  
        
        print(f'otp_entered: {otp_entered}, otp_generated: {otp_generated}')
        
        if otp_entered == otp_generated:
            return Response({'message': 'OTP validated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def viewprofile(request):
    if request.method == 'GET':
        user_id = request.user.id
        try:
            user = User.objects.get(id=user_id)
            user_serializer = UserSerializer(user)

            try:
                employee = Employee.objects.get(user=user)
                emp_serializer = EmployeeSerializers(employee)
                employeedata = {
                    'user': user_serializer.data,
                    'employee': emp_serializer.data
                }
                return Response(employeedata, status=status.HTTP_200_OK)
            except Employee.DoesNotExist:
                return Response({"message": "Employee not found for this user."}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Invalid Method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def editprofile(request):
    if request.method == 'PUT':
        user_instance = request.user
        user_data = request.data
        user_serializer = UserEditSerializersnew(instance=user_instance, data=user_data)
        employee_data = request.data
        employee_instance = user_instance.employee  
        employee_serializer = EmployeeEditSerializers(instance=employee_instance, data=employee_data)

        if user_serializer.is_valid(raise_exception=True) and employee_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            employee_serializer.save()

            response_data = {
                'user': user_serializer.data,
                'employee': employee_serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response({'error': user_serializer.errors, 'employee_error': employee_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'GET Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
        

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def categories(request):
    if request.method == 'GET':
        user = request.user.id
        categories = Category.objects.filter(user_id=user).order_by('-id')
        category_serializer = CategorySerializer(categories, many=True)
        return Response(category_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def subcategories(request, pk):
    if request.method == 'GET':
        subcategories = Subcategory.objects.filter(category_id=pk)
        subcategory_serializer = SubcategorySerializer(subcategories, many=True)
        return Response(subcategory_serializer.data, status=status.HTTP_200_OK)



@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class Expenses(APIView):
    def post(self, request):
        user = request.user  
        #print(user)
        request.data['user'] = user.id  
        serializer = ExpenseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk=None):  
        if pk is not None:  
            expense = Expense.objects.filter(id=pk).first()
            if expense:
                expense_serializer = ExpenseSerializerview(expense, context={'request': request})
                return Response(expense_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Expense not found'}, status=status.HTTP_404_NOT_FOUND)
        else:  
            user = request.user
            expenses = Expense.objects.filter(user=user)
            expenses_serializer = ExpenseSerializerNew(expenses, many=True)
            return Response(expenses_serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        expense = Expense.objects.filter(id=pk).first()
        if not expense:
            return Response({'message': 'Expense not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ExpenseSerializerEdit(instance=expense, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,  status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class Archive(APIView):   
    def get(self, request, pk=None):  
        if pk is not None:  
            expense = Expense.objects.filter(id=pk).first()
            if expense:
                expense_serializer = ExpenseSerializerview(expense, context={'request': request})
                return Response(expense_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Expense not found'}, status=status.HTTP_404_NOT_FOUND)
        else:  
            user = request.user
            expenses = Expense.objects.filter(user=user, archived=True)
            expenses_serializer = ExpenseSerializerNew(expenses, many=True)
            return Response(expenses_serializer.data, status=status.HTTP_200_OK)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class Viewreport(APIView):
    def get(self, request):
        user = request.user
        expenses = Expense.objects.filter(user=user, archived=False)
        
        # Get query parameters
        start_date = request.query_params.get('startdate')
        end_date = request.query_params.get('enddate')
        categories = request.query_params.getlist('categories')
        export_format = request.query_params.get('export', 'json')

        # Filter by start date
        if start_date:
            start_date = parse_date(start_date)
            if start_date:
                expenses = expenses.filter(expense_date__gte=start_date)
        
        # Filter by end date
        if end_date:
            end_date = parse_date(end_date)
            if end_date:
                expenses = expenses.filter(expense_date__lte=end_date)
        
        # Filter by categories
        if categories:
            expenses = expenses.filter(category__name__in=categories)
        
        if export_format == 'excel':
            domain = request.build_absolute_uri('/').rstrip('/')
            return self.export_to_excel(expenses, domain)
        else:
            # Serialize the filtered data
            expenses_serializer = ExpenseSerializerNew(expenses, many=True)
            return Response(expenses_serializer.data, status=status.HTTP_200_OK)

    def export_to_excel(self, expenses, domain):
        wb = Workbook()
        ws = wb.active
        ws.title = "Expense Report"

        # Write headers
        headers = ['Created Date', 'Expense Date', 'Category', 'Subcategory', 'Amount', 'Payment', 'Note', 'Proof', 'Document']
        for col, header in enumerate(headers, start=1):
            ws.cell(row=1, column=col, value=header)

        # Write data
        for row, expense in enumerate(expenses, start=2):
            ws.cell(row=row, column=1, value=expense.created_date)
            ws.cell(row=row, column=2, value=expense.expense_date)
            ws.cell(row=row, column=3, value=expense.category.name)
            ws.cell(row=row, column=4, value=expense.subcategory.name if expense.subcategory else '')
            ws.cell(row=row, column=5, value=expense.amount)
            ws.cell(row=row, column=6, value=expense.payment)
            ws.cell(row=row, column=7, value=expense.note)
            ws.cell(row=row, column=8, value=expense.proof)
            ws.cell(row=row, column=9, value=self.get_file_url(expense.document, domain))

        # Create a BytesIO buffer to save the workbook to
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        # Create the HttpResponse with Excel content type
        response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=expense_report.xlsx'

        return response

    def get_file_url(self, file, domain):
        if file and hasattr(file, 'name'):
            return f"{domain}{settings.MEDIA_URL}{file.name}"
        return ''

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class Archivereport(APIView):
    def get(self, request):
        user = request.user
        expenses = Expense.objects.filter(user=user)
        
        # Get query parameters
        start_date = request.query_params.get('startdate')
        end_date = request.query_params.get('enddate')
        categories = request.query_params.getlist('categories')
        export_format = request.query_params.get('export', 'json')

        # Filter by start date
        if start_date:
            start_date = parse_date(start_date)
            if start_date:
                expenses = expenses.filter(expense_date__gte=start_date)
        
        # Filter by end date
        if end_date:
            end_date = parse_date(end_date)
            if end_date:
                expenses = expenses.filter(expense_date__lte=end_date)
        
        # Filter by categories
        if categories:
            expenses = expenses.filter(category__name__in=categories)
        
        # Update filtered expenses to archived=True
        with transaction.atomic():
            updated_count = expenses.update(archived=True)
        
        if export_format == 'excel':
            return self.export_to_excel(expenses, request)
        else:
            # Serialize the filtered and updated data
            expenses_serializer = ExpenseSerializerNew(expenses, many=True)
            return Response({
                'message': f'{updated_count} expenses have been archived.',
                'archived_expenses': expenses_serializer.data
            }, status=status.HTTP_200_OK)

    def export_to_excel(self, expenses, request):
        wb = Workbook()
        ws = wb.active
        ws.title = "Archived Expense Report"

        # Write headers
        headers = ['Created Date', 'Expense Date', 'Category', 'Subcategory', 'Amount', 'Payment', 'Note', 'Proof', 'Document']
        for col, header in enumerate(headers, start=1):
            ws.cell(row=1, column=col, value=header)

        # Write data
        for row, expense in enumerate(expenses, start=2):
            ws.cell(row=row, column=1, value=expense.created_date)
            ws.cell(row=row, column=2, value=expense.expense_date)
            ws.cell(row=row, column=3, value=expense.category.name)
            ws.cell(row=row, column=4, value=expense.subcategory.name if expense.subcategory else '')
            ws.cell(row=row, column=5, value=expense.amount)
            ws.cell(row=row, column=6, value=expense.payment)
            ws.cell(row=row, column=7, value=expense.note)
            ws.cell(row=row, column=8, value=str(expense.proof) if expense.proof else '')
            ws.cell(row=row, column=9, value=self.get_file_url(expense.document, request))

        # Create a BytesIO buffer to save the workbook to
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        # Create the HttpResponse with Excel content type
        response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=archived_expense_report.xlsx'

        return response

    def get_file_url(self, file, request):
        if file and hasattr(file, 'name'):
            return request.build_absolute_uri(f"{settings.MEDIA_URL}{file.name}")
        return ''

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class Addsubcategory(APIView):
    def post(self, request):
        user = request.user.id 
        category = Category.objects.get(user=user, name='Miscellaneous')
        category_id = category.id
        request.data['category'] = category_id 
        request.data['user'] = user  
        serializer = AddsubcategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class Subscriptiondetails(APIView):
    def get(self, request):
        sub = Subscriptions.objects.exclude(id=1)
        subscriptions_serializer = SubscriptionSerialixer(sub, many=True)
        return Response(subscriptions_serializer.data, status=status.HTTP_200_OK)
    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class UserSubscriptionView(APIView):
    def get(self, request):
        user = request.user.id
        users=Usersubscription.objects.filter(user=user)
        subscriptio_serializer=UsersubscriptionSerializer(users, many=True)
        return Response(subscriptio_serializer.data, status=status.HTTP_200_OK)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class Subscriptionrenewal(APIView):
    def post(self, request):
        user = request.user
        sub_plan_id = request.data.get('sub_plan_id')

        # Fetch the subscription plan
        try:
            sub_plan = Subscriptions.objects.get(id=sub_plan_id)
        except Subscriptions.DoesNotExist:
            return Response({"error": "Subscription plan not found"}, status=404)

        # Check if the user has any active subscription
        active_subscription = Usersubscription.objects.filter(
            user=user,
            end_date__gte=timezone.now().date()
        ).first()

        if active_subscription:
            return Response({"error": "An active subscription already exists"}, status=400)

        # Calculate the new end date for a new subscription
        current_date = timezone.now().date()
        duration_days = sub_plan.duration_months * 30  # 1 month = 30 days
        new_end_date = current_date + timedelta(days=duration_days)

        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        amt = sub_plan.price
        status = request.data.get('status')

        # Create a new subscription record
        Usersubscription.objects.create(
            user=user,
            sub_plan=sub_plan,
            start_date=current_date,
            end_date=new_end_date,
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            amt=amt,
            status=status,
        )

        return Response({"message": "Subscription renewed successfully", "new_end_date": new_end_date})

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def dashboardanalysis(request):
    if request.method == 'GET':
        expenses = {
        "amount": 1964.00
        }
        category = {
        "Miscellaneous": 38.7,
        "Items Purchased": 20.69,
        "Food Expenses": 17.7,
        "Accommodation": 21.8,
        "Travel": 45
        }
        dashboarddtata = {
                    'expenses': expenses,
                    'category': category
                }
        return Response(dashboarddtata, status=status.HTTP_200_OK)
        
    else:
        return Response({'error': 'Invalid Method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class VerifyEmail(APIView):
    def get(self, request):
        email = request.user.email
        if email:
            otp = ''.join(random.choices(string.digits, k=6))
            cache.set(f'otp_{request.user.id}', otp, timeout=300)  # store OTP in cache for 5 minutes
            print(otp)
            send_mail(
                'OTP Verification For Delete Account',
                f'Your OTP is: {otp}',
                'Forgot Password OTP',
                [email],
                fail_silently=False,
            )
            return Response({'message': 'OTP sent to your email'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Email not provided'}, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class VerifyOTP(APIView):
    def post(self, request):
        otp = request.data.get('otp')
        cached_otp = cache.get(f'otp_{request.user.id}')

        if cached_otp is None:
            return Response({'error': 'OTP expired or not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        if otp == cached_otp:
            # OTP is correct, delete the user account
            request.user.delete()
            return Response({'message': 'Account deleted successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class Helpview(APIView):
    def get(self, request):
        help=Help.objects.all()
        help_serializer= HelpSerializer(help, many=True)
        return Response(help_serializer.data, status=status.HTTP_200_OK)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class Privacypolicy(APIView):
    def get(self, request):
        privacy_policies = PrivacyPolicy.objects.all()
        privacy_serializer= PrivacyPolicySerializer(privacy_policies, many=True)
        return Response(privacy_serializer.data, status=status.HTTP_200_OK)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])   
class Faqview(APIView):
    def get(self, request):
        faq = Faq.objects.all()
        faq_serializer = FaqSerializer(faq, many=True)
        return Response(faq_serializer.data, status=status.HTTP_200_OK)
    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])   
class Razorpaykeyview(APIView):
    def get(self, request):
        razorpay = Razorpaykey.objects.all()
        razorpay_serializer = RazorpaykeySerializer(razorpay, many=True)
        return Response(razorpay_serializer.data, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def forgotpassword(request):
    email = request.data.get('email')  
    if email:
        if User.objects.filter(email=email).exists():
            otp = ''.join(random.choices(string.digits, k=6))
            send_mail(
                'OTP Verification',
                f'Your OTP is: {otp}',
                'Forgot Password OTP',
                [email],
                fail_silently=False,
            )
            return Response({'message': 'OTP sent to your email', 'OTP': otp, 'email': email}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Email not found in the database'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Email not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def forgotpasswordotpvalidate(request):
    if request.method == 'POST':
        otp_entered = request.data.get('otp_entered')
        otp_generated = request.data.get('otp_generated')
        password = request.data.get('password')
        email = request.data.get('email')  
        user = User.objects.get(email=email)
        if otp_entered == otp_generated:
            user.password = make_password(password)
            user.save()
            return Response({'message': 'OTP Validated Successfully & Password Updated Successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
