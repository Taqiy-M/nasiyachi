from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

from .models import Customer, Category, Purchase, Payment, Staff, PurchaseItem


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class StaffSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Staff
        fields = ['id', 'user']


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = ['is_active']



class CustomerSerializerSpecial(ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name']



class PurchaseCreateSerializer(ModelSerializer):

    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = ["staff", "current_debt"]

    def validate(self, data):
        errors = {}
        # Check that required fields are not null
        for field_name in ['customer', 'created_date', 'product_name', 'original_price', 'nasiya_cost', 'product_category', 'base_price',
                           'purchase_description', 'interval_dates', 'first_payment', 'store']:
            if not data.get(field_name):
                errors[field_name] = f"{field_name} field is required"

        if errors:
            raise serializers.ValidationError(errors)
        return data


class PurchaseSerializer(ModelSerializer):
    customer = CustomerSerializerSpecial()
    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = ["staff", "current_debt"]

    def validate(self, data):
        errors = {}
        # Check that required fields are not null
        for field_name in ['customer', 'created_date', 'product_name', 'original_price', 'nasiya_cost', 'product_category', 'base_price',
                           'purchase_description', 'interval_dates', 'first_payment']:
            if not data.get(field_name):
                errors[field_name] = f"{field_name} field is required"

        if errors:
            raise serializers.ValidationError(errors)
        return data



class PurchaseItemSerializer(ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = ['date', 'completed', 'purchase']
        read_only_fields = ['date', 'completed', 'purchase']


class PaymentSerializer(ModelSerializer):
    staff = StaffSerializer(read_only = True)

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["staff"]

    def validate(self, data):
        errors = {}
        # Check that required fields are not null
        for field_name in ['purchase', 'money']:
            if not data.get(field_name):
                errors[field_name] = f"{field_name} field is required"

        if errors:
            raise serializers.ValidationError(errors)
        return data

