from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from sotuv.views import PurchaseViewSet, CustomerViewSet, CategoryViewSet, PaymentViewSet


router = routers.DefaultRouter()
router.register('purchases', PurchaseViewSet, basename='purchase')
router.register('customer', CustomerViewSet, basename='customer')
router.register('category', CategoryViewSet, basename='category')
router.register('payment', PaymentViewSet, basename='payment')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('obtain-token/', obtain_auth_token),
    # path('purchases/not-completed/', PurchaseViewSet.as_view({'get': 'not_completed'}), name='not-completed'),
    path('', include(router.urls))
]
