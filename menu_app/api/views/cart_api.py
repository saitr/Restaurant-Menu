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
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponse


LOGGER = logging.getLogger(__name__)

# Item api
class CartAPIList(APIView):

    def get(self,request):

        print("Inside get cart", request.query_params)
        table_number = request.query_params['table_name']
        cart_detail = Cart.objects.filter(table_number=table_number)
        cart_list = []
        for data in cart_detail:
            print("data.items", data.items)

            item_price = data.items.itemPrice
            return_dict = {'id': data.id,
                           'table_number': data.table_number,
                           'items': data.items,
                           'quantity': data.quantity,
                           'item_id': data.items_id,
                           'item_price': item_price
                           }

            cart_list.append(return_dict)

        context = {
            'return_list': cart_list,
            'table_name':table_number
        }
        print("context", context)
        # return Response(context, status=status.HTTP_200_OK)
        return render(request, 'cart.html', context)


    def post(self, request):
        print("inside  cart api post  ", request.data.get)

        print("inside  cart api post  ", request.data.get('table_name'))
        table_name = request.data.get('table_name')  # Get the value of 'table_name'
        item_id = request.data.get('item_id')
        print("item_id", item_id)

        post_set = {
        "table_number" : table_name,
        "items" : item_id,

        }

        try:
            get_cart_items = Cart.objects.get(table_number=table_name, items=item_id)
            print("**", get_cart_items.quantity)
            cart_item = get_cart_items  # Assuming there's only one item per table
            cart_item.quantity += 1
            cart_item.save()
        except Cart.DoesNotExist:
            self.db_utils_obj = DBUtils()
            self.db_utils_obj.set_serializer_object(
                model_serializer=CartSerializer,
                data_dict=post_set
            )

            # Assuming this saves the cart item

        category_name = Items.objects.filter(id=item_id).values('category__categoryName').first()
        print("category", category_name['category__categoryName'])

        # Return a JSON response
        url = 'http://127.0.0.1:8000/items?category={0}&table_name={1}'.format(category_name['category__categoryName'],table_name)
        # return redirect(url)

        return redirect(request.META.get('HTTP_REFERER', 'items'))

    def delete(self, request):

        print("inside delete cart item", request.data)
        table_number = request.data['table_name']
        item_id = request.data['item_id']
        print("table_number", table_number)
        print("item_id", item_id)

        try:
            cart_item = Cart.objects.get(table_number=table_number, items=item_id)

            # Decrease the quantity by 1 if it's greater than 1
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

            return HttpResponse("Order item deleted successfully.")

        except Cart.DoesNotExist:
            return HttpResponseBadRequest("Order item not found.")

