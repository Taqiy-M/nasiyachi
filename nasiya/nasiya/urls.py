from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from sotuv.views import PurchaseViewSet, CustomerViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register('purchases', PurchaseViewSet, basename='purchase')
router.register('customer', CustomerViewSet, basename='customer')
router.register('category', CategoryViewSet, basename='category')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('obtain-token/', obtain_auth_token),
    path('', include(router.urls))


]
