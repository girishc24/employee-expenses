from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response  import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from . serializers import UserAddSerializers, EmployeeSerializers, UserSerializer, UserAddSerializersnew
from .models import Employee


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