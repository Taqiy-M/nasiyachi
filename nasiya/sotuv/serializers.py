from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Customer, Category, Purchase, Payment


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = ['is_active']


class PurchaseSerializer(ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = ["staff", "current_debt"]

    def validate(self, data):
        errors = {}
        # Check that required fields are not null
        for field_name in ['customer', 'created_date', 'product_name', 'original_price', 'nasiya_cost',
                           'product_category', 'base_price',
                           'purchase_description', 'interval_dates', 'first_payment']:
            if not data.get(field_name):
                errors[field_name] = f"{field_name} field is required"

        if errors:
            raise serializers.ValidationError(errors)
        return data


class PaymentSerializer(ModelSerializer):
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
