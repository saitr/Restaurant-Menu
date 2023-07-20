from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import Items,Categories,Cart,Owner_Utility
import os
from ...serializers import ItemsSerializer
from django.core import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404
import json
import logging

LOGGER = logging.getLogger(__name__)

# Item api 
class ItemAPIList(APIView):

    def get(self, request):
        print("***", request.query_params)
        print("inside item get", request.query_params['category'])
        table_name = request.query_params['table_name']
        print("table_name", table_name)

        try:
            selected_category = Categories.objects.get(categoryName=request.query_params['category'])
            get_item = Items.objects.filter(category=selected_category)
        except Categories.DoesNotExist:
            get_item = []  #


        table = Owner_Utility.objects.get(table_number=table_name)
        print("table_number", table)

        cart_item_count = Cart.objects.filter(table_number_id=table, orderid_id__isnull=True,sub_order_id_id__order_place=None,cart_created=True).count()
        print("cart_item_count", cart_item_count)

        return_list = []
        for data in get_item:
            return_dict = {'item_id':data.id,
                           'category':data.category,
                           'itemName': data.itemName,
                           'itemPrice' : data.itemPrice,
                           'item_image': data.item_image,
                           'created_at':data.created_at,
                           'updated_at' : data.updated_at}

            return_list.append(return_dict)
        print("return_list", return_list)

        context = {
            'return_list': return_list,
            'table_name': request.query_params['table_name'],
            "cart_item_count": cart_item_count
        }
        print("context",context)
        return render(request, 'item.html', context)


    def patch(self, request):
        # Check if user is authenticated

        print("data in request", request.data)
        print("data in request", request.data.get('cart_id'))
        cart_id = request.data.get('cart_id')
        # Retrieve the cart item from the database
        cart_item = Cart.objects.get(pk=cart_id, user=request.user)

        # Update the quantity based on the action parameter
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                # If the quantity reaches 0, remove the item from the cart
                cart_item.delete()
                return redirect('cart_list')

        # Save the updated cart item
        cart_item.save()

    def delete(self,request):
        print("data in request", request.data)
        cart_id = request.data.get('cart_id')
        cart_delete = Cart.objects.filter(user=request.user)
        cart_delete.delete()
        return redirect('cart_list')


