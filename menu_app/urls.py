from django.urls import path
from menu_app.api.views.item_api import ItemAPIList
from menu_app.api.views.chef_api import ChefAPIList
from menu_app.api.views.category_api import CategoryAPIList
from menu_app.api.views.cart_api import CartAPIList
from menu_app.api.views.user_api import VerifyOTPView
from menu_app.api.views.varify_api import ValidateOTPView
from menu_app.api.views.order_item_api import OrderApiView
from menu_app.api.views.generatebarcode_api import GenerateBarcodeView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)

urlpatterns = [
    path('items', ItemAPIList.as_view() , name='items'),
    path('category_api/<int:variant>/', CategoryAPIList.as_view(),  name='category_api'),
    path('cart_api', CartAPIList.as_view(), name='cart_api'),
    path('user_api/', VerifyOTPView.as_view(),  name='user_api'),
    path('varify_api/', ValidateOTPView.as_view(),  name='varify_api'),
    path('order_api/', OrderApiView.as_view(),  name='order_api'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('generate_barcode/', GenerateBarcodeView.as_view(), name='generate_barcode'),
    path('chef_api/', ChefAPIList.as_view(), name='chef_api'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

