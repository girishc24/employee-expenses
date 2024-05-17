from rest_framework import serializers
from . models import Employee, Category, Subcategory, Expense, Subscriptions, Help, PrivacyPolicy,Faq, Usersubscription
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from djoser.serializers  import UserSerializer, UserCreateSerializer

class UserAddSerializers(serializers.ModelSerializer):
    class  Meta:
        model  =  User
        fields = ['id','first_name','last_name','email','password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, attrs):
        attrs['username'] = attrs['email']  
        return attrs

    def save(self, **kwargs):
        password = self.validated_data.get('password')
        if password:  # Check if password is provided
            self.validated_data['password'] = make_password(password)  # Hash the password using make_password
        return super().save(**kwargs)


class UserAddSerializersnew(serializers.ModelSerializer):
    class  Meta:
        model  =  User
        fields = ['id','first_name','last_name','email']
        


class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields= ['phone','designation','company','photo']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username',  'email', 'first_name', 'last_name',]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id','name']


class ExpenseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Expense
        fields = ['id', 'document', 'created_date', 'updated_date', 'expense_date', 'amount', 'category', 'subcategory', 'payment', 'note', 'proof','user','document']

class ExpenseSerializerview(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubcategorySerializer()
    class Meta:
        model = Expense
        fields = ['id', 'document', 'created_date', 'updated_date', 'expense_date', 'amount', 'category', 'subcategory', 'payment', 'note', 'proof','user','document']


class ExpenseSerializerNew(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubcategorySerializer()
    class Meta:
        model = Expense
        fields = [ 'id','expense_date', 'amount', 'category', 'subcategory', 'payment']

class ExpenseSerializerEdit(serializers.ModelSerializer):
    
    class Meta:
        model = Expense
        fields = ['id', 'document', 'created_date', 'updated_date', 'expense_date', 'amount', 'category', 'subcategory', 'payment', 'note', 'proof','document']

    

class SubscriptionSerialixer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = '__all__'

class UsersubscriptionSerializer(serializers.ModelSerializer):
    #user = UserSerializer()
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

class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = '__all__'