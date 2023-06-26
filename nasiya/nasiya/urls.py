from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from sotuv.views import PurchaseViewSet, CustomerViewSet, CategoryViewSet, PaymentViewSet, PurchaseItemViewSet
from drf_yasg import openapi


from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version="v1",
        description="My API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)




router = routers.DefaultRouter()
router.register('purchases', PurchaseViewSet, basename='purchase')
router.register('customer', CustomerViewSet, basename='customer')
router.register('category', CategoryViewSet, basename='category')
router.register('payment', PaymentViewSet, basename='payment')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('purchases/<int:purchase_id>/pay_dates/', PurchaseItemViewSet.as_view({'get': 'list'}), name='purchaseitem-list'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('obtain-token/', obtain_auth_token),
    # path('purchases/not-completed/', PurchaseViewSet.as_view({'get': 'not_completed'}), name='not-completed'),
    path('', include(router.urls)),

]
