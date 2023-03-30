from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Purchase)
admin.site.register(Payment)
admin.site.register(Staff)
admin.site.register(PurchaseItem)
