from rest_framework import serializers
from . models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from djoser.serializers  import UserSerializer, UserCreateSerializer
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Sum
import math

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])
        data['access_expiry'] = refresh.access_token.payload['exp']
        return data

class UserCreateSerializer(serializers.ModelSerializer):
    class  Meta:
        model  =  User
        fields = ['id','first_name','last_name','email','password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, attrs):
        attrs['username'] = attrs['email']  
        return attrs

    def save(self, **kwargs):
        password = self.validated_data.get('password')
        if password:  
            self.validated_data['password'] = make_password(password)  
        return super().save(**kwargs)


class UserAddSerializersnew(serializers.ModelSerializer):
    class  Meta:
        model  =  User
        fields = ['id','first_name','last_name','email']

class UserEditSerializersnew(serializers.ModelSerializer):
    class  Meta:
        model  =  User
        fields = ['id','first_name','last_name','password'] 
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
            
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance   
    
    def save(self, **kwargs):
        password = self.validated_data.get('password')
        if password:  
            self.validated_data['password'] = make_password(password)  # Hash the password using make_password
        return super().save(**kwargs) 

class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields= ['phone','designation','company','photo','department','emp_id']

class EmployeeEditSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['designation', 'company', 'photo', 'department', 'emp_id']
        extra_kwargs = {
            'designation': {'required': False},
            'company': {'required': False},
            'photo': {'required': False},
            'department': {'required': False},
            'emp_id': {'required': False},
        }

    def update(self, instance, validated_data):
        photo = validated_data.pop('photo', None)
        if photo:
            instance.photo = photo
        return super().update(instance, validated_data)
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username',  'email', 'first_name', 'last_name']

class CategorySerializer(serializers.ModelSerializer):
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'photo', 'percentage']

    def get_percentage(self, obj):
        user_id = self.context['request'].user.id
        total_expense = Expense.objects.filter(user_id=user_id, archived=False).aggregate(Sum('amount'))['amount__sum'] or 0
        
        if obj:
            category_expense = Expense.objects.filter(user_id=user_id, archived=False, category=obj).aggregate(Sum('amount'))['amount__sum'] or 0
            percentage = (category_expense / total_expense) if total_expense else 0
            return round(percentage, 2)  # Ensure the percentage is represented as a float to two decimal places
        
        return 0.0

class CategoriesWithTotalExpenseSerializer(serializers.Serializer):
    category = CategorySerializer(many=True)

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id','name']

class AddsubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id','category','name','user']

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'document', 'created_date', 'updated_date', 'expense_date', 'amount', 'category', 'subcategory', 'payment', 'note', 'proof', 'user']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class ExpenseSerializerview(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubcategorySerializer()
    
    class Meta:
        model = Expense

        fields = ['id', 'document', 'created_date', 'updated_date', 'expense_date', 'amount', 'category', 'subcategory', 'payment', 'note', 'proof', 'user']

    def get_document_url(self, obj):
        request = self.context.get('request')
        if request and obj.document:
            return request.build_absolute_uri(settings.MEDIA_URL + obj.document)
        return None


    def get_document_url(self, obj):
        request = self.context.get('request')
        if obj.document:
            return request.build_absolute_uri(obj.get_document_url())
        return None
    
class ExpenseSerializerNew(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubcategorySerializer()
    class Meta:
        model = Expense
        fields = [ 'id','expense_date', 'amount', 'category', 'subcategory', 'payment']

    

class ExpenseSerializerEdit(serializers.ModelSerializer):
    
    class Meta:
        model = Expense
        fields = ['id',  'created_date', 'updated_date', 'expense_date', 'amount', 'category', 'subcategory', 'payment', 'note', 'proof','document']
        extra_kwargs = {
                'document': {'required': False},
                'expense_date': {'required': False},
                'amount': {'required': False},
                'category': {'required': False},
                'subcategory': {'required': False},
                'payment': {'required': False},
                'note': {'required': False},
                'proof': {'required': False},
            }
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def get_document_url(self, obj):
        request = self.context.get('request')
        if obj.document:
            return request.build_absolute_uri(obj.get_document_url())
        return None


class SubscriptionSerialixer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = '__all__'

class SubscriptionSerialixerNew(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = [ 'id','name', 'description']

class UsersubscriptionSerializer(serializers.ModelSerializer):
    sub_plan = SubscriptionSerialixerNew()
    class Meta:
        model = Usersubscription
        fields ='__all__'



class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = '__all__'

class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'

class TermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Termscondition
        fields = '__all__'

class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = '__all__'


class RazorpaykeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Razorpaykey
        fields = '__all__'
