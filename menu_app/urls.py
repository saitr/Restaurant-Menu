from django.urls import path
from menu_app.api.views.item_api import ItemAPIList
from menu_app.api.views.category_api import CategoryAPIList
from menu_app.api.views.cart_api import CartAPIList
from menu_app.api.views.user_api import VerifyOTPView


urlpatterns = [
    path('items/', ItemAPIList.as_view()),
    path('category_api/', CategoryAPIList.as_view(),  name='category_api'),
    path('cart_api/', CartAPIList.as_view()),
    path('user_api/', VerifyOTPView.as_view(),  name='user_api'),

]