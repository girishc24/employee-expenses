from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response  import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from . serializers import UserAddSerializers, EmployeeSerializers, UserSerializer, UserAddSerializersnew, CategorySerializer, SubcategorySerializer, ExpenseSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee,Category, Subcategory,  Expense



def welcome(request):
    return  HttpResponse("Welcome")

@api_view(['POST'])
def adduser(request):
    if request.method == 'POST':
        user_serializer = UserAddSerializers(data=request.data)
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


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def viewprofile(request):
    if request.method == 'GET':
        user = request.user.id
        queryset = User.objects.filter(id=user)
        user_serializers = UserSerializer(queryset, many=True)

        try:
            employee = Employee.objects.get(user=user)
            emp_serializers = EmployeeSerializers(employee)
            employeedata = {
                'user': user_serializers.data,
                'employee': emp_serializers.data
            }
            return Response(employeedata)
        except Employee.DoesNotExist:
            return Response({"message": "Employee not found for this user."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Invalid Method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def editprofile(request):
    if request.method == 'PUT':
        user_instance = request.user
        user_data = request.data.get('user', {})
        user_data['username'] = user_data.get('email')  # Set email as the username
        user_serializer = UserAddSerializersnew(instance=user_instance, data=user_data)
        employee_instance = user_instance.employee
        employee_serializer = EmployeeSerializers(instance=employee_instance, data=request.data.get('employee', {}))

        user_valid = user_serializer.is_valid()
        employee_valid = employee_serializer.is_valid()

        if user_valid and employee_valid:
            user_serializer.save()
            employee_serializer.save()
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        else:
            errors = {
                'user_errors': user_serializer.errors if not user_valid else None,
                'employee_errors': employee_serializer.errors if not employee_valid else None
            }
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

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
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user = request.user.id
        expenses = Expense.objects.filter(user_id=user)
        expenses_serializer = ExpenseSerializer(expenses, many=True)
        return Response(expenses_serializer.data, status=status.HTTP_200_OK)



class Addcategory(APIView):
    def post(request):
        pass