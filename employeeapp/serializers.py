from rest_framework import serializers
from . models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from djoser.serializers  import UserSerializer, UserCreateSerializer
from django.conf import settings

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
            self.validated_data['password'] = make_password(password)  # Hash the password using make_password
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
        fields= ['phone','designation','company','photo']

class EmployeeEditSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields= ['designation','company','photo']
        extra_kwargs = {
            'designation': {'required': False},
            'company': {'required': False},
            'photo': {'required': False},
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
    class Meta:
        model = Category
        fields = ['id','name']

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
        fields = ['id', 'document',  'created_date', 'updated_date', 'expense_date', 'amount', 'category', 'subcategory', 'payment', 'note', 'proof','user','document']
    
    def get_document_url(self, obj):
        request = self.context.get('request')
        if obj.document:
            return request.build_absolute_uri(obj.get_document_url())
        return None
    

    def get_document_url(self, obj):
        request = self.context.get('request')
        if obj.document:
            return request.build_absolute_uri(obj.get_document_url())
        return None

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
