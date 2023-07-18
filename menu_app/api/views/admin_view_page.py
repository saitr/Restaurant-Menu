from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import Cart,Items
import os
from ...serializers import CartSerializer
from django.core import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404
import json
import logging
from .utils.database_helper import DBUtils
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from ...models import CustomUser, Cart, Order_Items, Order,Owner_Utility,SubOrder
from ...serializers import SubOrderSerializer
from django.shortcuts import render, redirect
from menu_app.api.views.utils.database_helper import DBUtils
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAdminUser
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password

LOGGER = logging.getLogger(__name__)

# Item api
class AdminDetailAPIList(APIView):



    def get(self, request):
            permission_classes = [IsAdminUser]
            print("INSIDE GET OF ORDER ITEM for Admin", request.query_params)
            print("INSIDE GET OF ORDER ITEM for Admin", request)
            password = request.query_params['password']
            phone_number = request.query_params['phone_number']

            try:
                user = CustomUser.objects.get(phone_number=phone_number)
                print("User", user.password)
                print("User", password)
                print("super", user.is_superuser)
            except CustomUser.DoesNotExist:
                user = None

            if user is not None and check_password(password, user.password)and user.is_superuser:

                print("valid")
                cart_items = Cart.objects.filter(orderid__generate_bill=False)
                print("cart_items", cart_items)
                return_list = []
                order_dict = {}
                list_item = []

                for item in cart_items:
                    item_data = {
                        "sub_order_id": item.sub_order_id_id,
                        "item_name": item.items.itemName,
                        "table_name": item.table_number.table_number,
                        "item": item.items,
                        "quantity": item.quantity,
                        "order_id": item.orderid_id
                    }
                    list_item.append(item_data)

                order_dict = {}

                for item in list_item:
                    order_id = item['order_id']
                    sub_order_id = item['sub_order_id']
                    if order_id not in order_dict:
                        order_dict[order_id] = {}
                    if sub_order_id not in order_dict[order_id]:
                        order_dict[order_id][sub_order_id] = []
                    order_dict[order_id][sub_order_id].append(item)

                grouped_data = []
                for order_id, sub_orders in order_dict.items():
                    order_data = {'order_id': order_id, 'sub_orders': []}
                    for sub_order_id, sub_order_items in sub_orders.items():
                        sub_order_data = {'sub_order_id': sub_order_id, 'items': sub_order_items}
                        order_data['sub_orders'].append(sub_order_data)
                    grouped_data.append(order_data)

                context = {
                    'return_list': grouped_data
                }
                print("context", context)
                # Clear the error message from the session
                messages.get_messages(request).used = True
                return render(request, 'admin_detail.html', context)

            else:
                print("invalid")
                messages.error(request, 'Invalid credentials')  # Add error message to Django messages framework

                # Pass the error message to the template
                return render(request, 'admin_login.html', {'error_message': 'Invalid credentials'})