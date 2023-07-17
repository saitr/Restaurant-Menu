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
            price_dict = {}
            for item in order_item_obj:
                print("item price", item.order_item_price)
                print("item quantity", item.quantity)
                print("item name", item.item_id.itemName)
                items_dict[item.item_id.itemName] += item.quantity  # Aggregate quantities by item name
                total_price += item.order_item_price * item.quantity
                price_dict.update({"item.item_id.itemName": item.order_item_price})

            items = []
            for item_name, quantity in items_dict.items():

                items.append({
                    "Item": item_name,
                    "Quantity": quantity,
                })
            print("items_dict", items_dict)
            print("items", items)


            items_with_price = []

            for item in items:
                item_name = item['Item']
                quantity = item['Quantity']

                # Find the corresponding item in order_item_obj
                item_obj = Order_Items.objects.filter(item_id__itemName=item_name, orderid=order_id).first()

                if item_obj:
                    item_price = item_obj.order_item_price
                    item['ItemPrice'] = item_price
                else:
                    item['ItemPrice'] = None




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