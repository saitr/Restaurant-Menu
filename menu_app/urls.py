from django.urls import path
from menu_app.api.views.item_api import ItemAPIList
from menu_app.api.views.first_page import FirstPageAPIList
from menu_app.api.views.chef_api import ChefAPIList
from menu_app.api.views.category_api import CategoryAPIList
from menu_app.api.views.cart_api import CartAPIList
from menu_app.api.views.user_api import VerifyOTPView
from menu_app.api.views.admin_login_api import AdminLoginDetailAPIList
from menu_app.api.views.varify_api import ValidateOTPView
from menu_app.api.views.order_item_api import OrderApiView
from menu_app.api.views.admin_view_page import AdminDetailAPIList
from menu_app.api.views.index import indexAPIList
from menu_app.api.views.home import HomeAPIList
from menu_app.api.views.notification_api import NotificationAPIList
from menu_app.api.views.owner_utility import Owner_UtilityView
from menu_app.api.views.generate_bill import GenerateBillAPIList
from menu_app.api.views.generatebarcode_api import GenerateBarcodeView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)

urlpatterns = [
    path('items', ItemAPIList.as_view() , name='items'),
    path('home', HomeAPIList.as_view() , name='home'),
    path('first_page/<int:variant>/', FirstPageAPIList.as_view() , name='home'),
    path('admin_view_page', AdminDetailAPIList.as_view() , name='admin_view_page'),
    path('notification_api', NotificationAPIList.as_view() , name='notification_api'),
    path('admin_login_api', AdminLoginDetailAPIList.as_view() , name='admin_login_api'),
    path('generate_bill', GenerateBillAPIList.as_view() , name='generate_bill'),
    path('admin_utiliti/<int:pk>/', Owner_UtilityView.as_view() , name='admin_utiliti'),
    path('category_api/<int:variant>/', CategoryAPIList.as_view(),  name='category_api'),
    path('cart_api', CartAPIList.as_view(), name='cart_api'),
    path('user_api/', VerifyOTPView.as_view(),  name='user_api'),
    path('varify/', ValidateOTPView.as_view(),  name='varify'),
    path('order_api/', OrderApiView.as_view(),  name='order_api'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('generate_barcode/', GenerateBarcodeView.as_view(), name='generate_barcode'),
    path('chef_api/', ChefAPIList.as_view(), name='chef_api'),
    path('index/<int:variant>/', indexAPIList.as_view(), name='index'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

