from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Purchase, Customer, Category, PurchaseItem, Staff
from .serializers import PurchaseSerializer, CustomerSerializer, CategorySerializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]


class PurchaseViewSet(ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]


    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # getting purchase that we are creating from api request
        # and assigning its staff
        id_of_purchase = response.data['id']
        created_purchase = Purchase.objects.get(pk=id_of_purchase)
        created_purchase.staff = Staff.objects.get(user=request.user)


        # getting intervals as a list
        intervals = created_purchase.interval_dates.split(',')


        # getting remainder debt which is a = cost - first_payment
        # then we use this remainder in following loop
        a = created_purchase.product_cost - created_purchase.first_payment
        created_purchase.current_debt = a
        rem = a - created_purchase.base_price


        created_purchase.save()
        # creating several PurchaseItems and assigning their dates
        while rem > 0:
            # datee =
            PurchaseItem.objects.create(purchase=created_purchase, completed=False, remainder_debt=rem)
            rem = rem - created_purchase.base_price
        return response






