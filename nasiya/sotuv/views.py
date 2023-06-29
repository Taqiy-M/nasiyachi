import datetime

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Purchase, Customer, Category, PurchaseItem, Staff, Payment, PurchaseItem
from .serializers import PurchaseSerializer, PurchaseCreateSerializer, CustomerSerializer, CategorySerializer, PaymentSerializer, PurchaseItemSerializer
from rest_framework import status
from django.core.exceptions import FieldError


class CustomModelViewSet(ModelViewSet):
    def handle_exception(self, exc):
        if isinstance(exc, FieldError):
            return self.handle_field_error(exc)
        if isinstance(exc, AttributeError):
            return self.handle_attribute_error(exc)
        if isinstance(exc, ValueError):
            return self.handle_value_error(exc)
        return super().handle_exception(exc)

    def handle_field_error(self, exc):
        return Response(
            {'detail': 'Invalid field name: {}'.format(str(exc))},
            status=status.HTTP_400_BAD_REQUEST
        )

    def handle_attribute_error(self, exc):
        return Response(
            {'detail': 'Invalid attribute: {}'.format(str(exc))},
            status=status.HTTP_400_BAD_REQUEST
        )

    def handle_value_error(self, exc):
        return Response(
            {'detail': 'Invalid value: {}'.format(str(exc))},
            status=status.HTTP_400_BAD_REQUEST
        )

class CustomerViewSet(CustomModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'passport_num', 'phone_num']
    pagination_class = PageNumberPagination


    @action(detail=True, methods=['get'])
    def purchases(self, request, pk=None):
        customer = self.get_object()
        purchases = customer.purchases.all()
        serializer = PurchaseSerializer(purchases, many=True)
        return Response(serializer.data)



class CategoryViewSet(CustomModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]


class PurchasePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PurchaseViewSet(CustomModelViewSet):
    queryset = Purchase.objects.all().order_by('-created_date')
    authentication_classes = [TokenAuthentication]
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PurchasePagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['customer__name', 'product_name']
    search_fields = ['customer__name', 'product_name']


    def get_serializer_class(self):
        if self.action == 'create':
            return PurchaseCreateSerializer
        return PurchaseSerializer

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
        purchases = Purchase.objects.filter(purchaseitem__in=purchase_items).distinct().order_by('-created_date')

        # Apply pagination
        page = self.paginate_queryset(purchases)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(purchases, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'])
    def not_completed(self, request):
        search_keyword = request.query_params.get('search')
        if search_keyword:
            queryset=Purchase.objects.filter(product_name__contains=search_keyword, completed=False).order_by('-created_date')
        else:
            queryset = Purchase.objects.filter(completed=False).order_by('-created_date')

        # Apply pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'])
    def completed(self, request):
        search_keyword = request.query_params.get('search')
        if search_keyword:
            queryset=Purchase.objects.filter(Q(product_name__contains=search_keyword, completed=True) |
            Q(customer__name__contains=search_keyword, completed=True)).order_by('-created_date')
        else:
            queryset = Purchase.objects.filter(completed=True).order_by('-created_date')

        # Apply pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['GET'], url_path='category/(?P<category_id>\d+)')
    def category(self, request, category_id=None):
        search_keyword = request.query_params.get('search')
        if search_keyword:
            purchases=Purchase.objects.filter(Q(product_name__contains=search_keyword, product_category_id=category_id) |
            Q(customer__name__contains=search_keyword, product_category_id=category_id)).order_by('-created_date')
        else:
            # Filter purchases based on the specified category ID
            purchases = Purchase.objects.filter(product_category_id=category_id).order_by('-created_date')



        # Apply pagination
        page = self.paginate_queryset(purchases)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(purchases, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        purchase = self.get_object()
        payments = purchase.payments.order_by('-date', '-id')

        # Apply pagination
        page = self.paginate_queryset(payments)
        if page is not None:
            serializer = PaymentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

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
        #next_payment_integer_id = intervals.index(created_purchase.next_payment_date)
        # shu joyda FRONT-END chi hal qilishi kerak bo'lgan ish bor:
        # masalan, interval uchun 3 ta sana belgilansa,
        # next_payment_date shu 3 tadan bittasi bo'lishi shart!!!

        # getting remainder debt which is a = cost - first_payment
        # then we use this remainder in following loop
        a = created_purchase.nasiya_cost - created_purchase.first_payment
        created_purchase.current_debt = a
        rem = a - created_purchase.base_price


        created_purchase.save()
        start_date = created_purchase.next_payment_date
        PurchaseItem.objects.create(purchase=created_purchase, completed=False, remainder_debt=rem, date=start_date)

        a = intervals.index(start_date.day)

        # creating several PurchaseItems and assigning their dates
        day = start_date.day
        month = start_date.month
        year = start_date.year
        while rem-created_purchase.base_price >= 0:
            if intervals[-1] == intervals[a % len(intervals)]:
                month = (month % 12) + 1
                if month == 1:
                    year += 1
            day = intervals[a % len(intervals)]
            a = a + 1
            datee = datetime.datetime(day=day, month=month, year=year)
            rem = rem - created_purchase.base_price
            PurchaseItem.objects.create(purchase=created_purchase, completed=False, remainder_debt=rem, date=datee)
        try:
            created_purchase.final_payment_date = datee
        except:
            created_purchase.final_payment_date = start_date
        created_purchase.save()
        return response


class PaymentViewSet(CustomModelViewSet):
    queryset = Payment.objects.all().order_by('-date', '-id')
    serializer_class = PaymentSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    pagination_class = PageNumberPagination

    # @action(detail=True, methods=['get'])
    # def for_purchase(self, request, pk=None):
    #     purchase = Purchase.objects.get(pk=pk)
    #     queryset = Payment.objects.filter(purchase=purchase)
    #     serializer = PaymentSerializer(queryset, many=True)
    #     return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        purchase_id = request.data.get('purchase')
        purchase = get_object_or_404(Purchase, id=purchase_id)

        if purchase.completed:
            return Response({'detail': 'Cannot create payment for a completed purchase.'}, status=status.HTTP_400_BAD_REQUEST)

        response = super().create(request, *args, **kwargs)
        id_of_payment = response.data['id']
        money = response.data['money']

        created_payment = Payment.objects.get(pk=id_of_payment)
        created_payment.staff = Staff.objects.get(user=request.user)
        # purchase = Purchase.objects.get(id=response.data['purchase'])
        purchase = get_object_or_404(Purchase, id=response.data['purchase'])
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


class PurchaseItemViewSet(viewsets.ModelViewSet):
    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer

    def get_queryset(self):
        purchase_id = self.kwargs['purchase_id']
        return get_object_or_404(Purchase, pk=purchase_id).purchaseitem_set.all().order_by('date')