from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import Items,Categories,Cart,Order,Order_Items,SubOrder
import os
from ...serializers import ItemsSerializer
from django.core import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404
import json
import logging
from django.http import HttpResponse
from collections import defaultdict

LOGGER = logging.getLogger(__name__)



# Item api
class GenerateBillAPIList(APIView):


    def get(self, request):
        print("Inside Get bill generate", request.GET.get)
        table_name = request.GET.get('table_number')
        order_id = request.GET.get('order_id')
        print("table_name", table_name)
        print("order_id", order_id)
        try:
            order_obj = Order.objects.get(id=order_id)
            print("order_obj", order_obj)

            items_dict = defaultdict(int)  # Use defaultdict to aggregate quantities by item ID
            total_price = 0

            order_item_obj = Order_Items.objects.filter(orderid=order_id)
            for item in order_item_obj:
                items_dict[item.item_id.itemName] += item.quantity  # Aggregate quantities by item name
                total_price += item.order_item_price * item.quantity

            items = []
            for item_name, quantity in items_dict.items():
                items.append({
                    "Item": item_name,
                    "ItemPrice": order_item_obj[0].order_item_price,  # Use any price from the order_item_obj
                    "Quantity": quantity,
                })

            return_dict = {
                "table_number": order_obj.table_number,
            }

            context = {
                "order_id": order_id,
                "table_name": table_name,
                "order_details": return_dict,
                "items": items,
                "total_price": total_price
            }

            print("request", request)
            order_obj.generate_bill = True
            order_obj.total_price = total_price
            order_obj.save()
            return render(request, 'download_bill.html', context)

        except Order.DoesNotExist:
            return {
                'error': 'Order does not exist.',
            }