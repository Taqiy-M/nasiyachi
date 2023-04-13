import datetime

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Purchase, Customer, Category, PurchaseItem, Staff, Payment
from .serializers import PurchaseSerializer, CustomerSerializer, CategorySerializer, PaymentSerializer


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

    @action(detail=False, methods=['GET'], url_path='between-dates')
    def get_purchases_between_dates(self, request):
        # Get the start and end dates from query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Convert the string dates to datetime objects
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Get all PurchaseItems that have a date between the start and end dates and completed is False
        purchase_items = PurchaseItem.objects.filter(date__range=[start_date, end_date], completed=False)

        # Get all the unique Purchase objects for the filtered PurchaseItems
        purchases = Purchase.objects.filter(purchaseitem__in=purchase_items).distinct()

        # Serialize the Purchase objects and return the response
        serializer = PurchaseSerializer(purchases, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'])
    def not_completed(self, request):
        queryset = Purchase.objects.filter(completed=False)
        serializer = PurchaseSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        purchase = self.get_object()
        payments = purchase.payments.order_by('date')
        print(payments)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # getting purchase that we are creating from api request
        # and assigning its staff
        id_of_purchase = response.data['id']
        created_purchase = Purchase.objects.get(pk=id_of_purchase)
        created_purchase.staff = Staff.objects.get(user=request.user)


        # getting intervals as a list

        intervals = list(map(int, created_purchase.interval_dates.replace(" ", "").split(',')))
        next_payment_integer_id = intervals.index(created_purchase.next_payment_date)
        # shu joyda FRONT-END chi hal qilishi kerak bo'lgan ish bor:
        # masalan, interval uchun 3 ta sana belgilansa,
        # next_payment_date shu 3 tadan bittasi bo'lishi shart!!!

        # getting remainder debt which is a = cost - first_payment
        # then we use this remainder in following loop
        a = created_purchase.product_cost - created_purchase.first_payment
        created_purchase.current_debt = a
        rem = a - created_purchase.base_price


        created_purchase.save()
        tday = datetime.date.today()
        month = 0
        year = 0
        if intervals[-1] > tday.day:
            month = tday.month
            year = tday.year
        else:
            if month == 12:
                month = 1
                year += 1
            else:
                month += 1


        # creating several PurchaseItems and assigning their dates
        while rem >= 0:
            a = next_payment_integer_id % len(intervals)
            datee = datetime.date(year=year, month=month, day=intervals[a])
            if intervals[-1] == intervals[a]:
                month = (month % 12) + 1
                if month == 1:
                    year += 1
            print(f'{datee}=================================')
            print(month)
            print(f'{datee}==================================')
            PurchaseItem.objects.create(purchase=created_purchase, completed=False, remainder_debt=rem, date=datee)
            rem = rem - created_purchase.base_price
            next_payment_integer_id += 1

        try:
            created_purchase.last_payment_date = datee
        except:
            a = next_payment_integer_id % len(intervals)
            datee = datetime.date(year=year, month=month, day=intervals[a])
            created_purchase.last_payment_date = datee
        created_purchase.save()
        return response


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    #
    # @action(detail=True, methods=['get'])
    # def for_purchase(self, request, pk=None):
    #     purchase = Purchase.objects.get(pk=pk)
    #     queryset = Payment.objects.filter(purchase=purchase)
    #     serializer = PaymentSerializer(queryset, many=True)
    #     return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        id_of_payment = response.data['id']
        money = response.data['money']
        created_payment = Payment.objects.get(pk=id_of_payment)
        created_payment.staff = Staff.objects.get(user=request.user)

        purchase = Purchase.objects.get(id=response.data['purchase'])
        purchase.current_debt -= money
        if purchase.current_debt <= 0:
            purchase.completed = True
        items = PurchaseItem.objects.filter(purchase=purchase, completed=False)
        purchase.save()
        created_payment.save()

        for i in range(len(items)):
            if items[i].remainder_debt >= purchase.current_debt:
                items[i].completed = True
                items[i].save()
            else:
                break


        return response


