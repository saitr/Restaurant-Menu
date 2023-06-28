from django.urls import path
from menu_app.api.views.item_app import ItemAPIList


urlpatterns = [
    path('items/', ItemAPIList.as_view()),
]