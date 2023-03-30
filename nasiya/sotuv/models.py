from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    passcode = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    name = models.CharField(max_length=30)
    passport_num = models.CharField(max_length=9, null=True)
    phone_num = models.CharField(max_length=30)


    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    photo = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    created_date = models.DateField(null=True, blank=True)
    product_name = models.CharField(max_length=50, null=True, blank=True)
    product_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    product_cost = models.IntegerField(null=True, blank=True, default=0)
    base_price = models.IntegerField(null=True, blank=True, default=0)
    purchase_description = models.TextField(null=True, blank=True)
    interval_dates = models.CharField(max_length=50, default="10")
    not_completed = models.BooleanField(default=True, null=True)
    first_payment = models.PositiveIntegerField(null=True, default=0)
    current_debt = models.PositiveIntegerField(null=True)
    next_payment_date = models.PositiveIntegerField()

    def __str__(self):
        return self.customer.name


class PurchaseItem(models.Model):
    # For one purchase, we have several PurchaseItems
    # For example if we have product_cost = 400$ and base_price 50$ each month
    # then we have to create 400/50 = 8 PurchaseItems
    # For example, if we give interval dates as "10,15" then dates of PurchaseItem will be
    # every 10th and 15th days of months starting from creating dates.
    # We may have only one problem: for example, if we have "10,20" as interval dates
    # and current date is 15th, then first payment should be done on 20th, not 10th.
    # we have to handle this issue inside create method of our PurchaseViewSet.

    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField()
    remainder_debt = models.PositiveIntegerField()


class Payment(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    purchase = models.ForeignKey(Purchase, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    money = models.IntegerField(default=0)
    date = models.DateTimeField()
    phone = models.CharField(max_length=30)

    def __str__(self):
        return self.purchase.customer.name






