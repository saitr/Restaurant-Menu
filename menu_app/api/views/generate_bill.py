from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import Items,Categories,Cart,Order,Order_Items
import os
from ...serializers import ItemsSerializer
from django.core import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404
import json
import logging
from django.http import HttpResponse

LOGGER = logging.getLogger(__name__)



# Item api
class GenerateBillAPIList(APIView):

    def get(self, request):
        print("Inside Get bill generate",request.GET.get)
        table_name =  request.GET.get('table_number')
        order_id =  request.GET.get('order_id')
        print("table_name", table_name)
        print("order_id", order_id)
        order_obj = Order.objects.get(id=order_id)
        print("order_obj", order_obj)
        order_obj.generate_bill = True
        order_obj.order_deliverd = True
        order_obj.save()

        return_dict = {
            "table_number": order_obj.table_number,
            "total_price": order_obj.total_price,
            "order_deliverd": order_obj.order_deliverd

        }
        order_item_obj = Order_Items.objects.filter(orderid=order_id)
        items = []
        for item in order_item_obj:
            items.append({
                "Item": item.item_id.itemName,
                "ItemPrice": item.order_item_price,
                "Quantity": item.quantity,
            })

        context = {
            "order_id": order_id,
            "table_name": table_name,
            "order_details": return_dict,
            "items": items,
        }
        print("request", request)

        return render(request, 'download_bill.html', context)


