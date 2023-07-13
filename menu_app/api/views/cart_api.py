from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import Cart,Items,Owner_Utility
from django.db.models import Q
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

        print("Inside get cart")
        table_number = request.query_params['table_name']
        table = Owner_Utility.objects.get(table_number=table_number)
        print("table_number", table)
        cursor, connection = DBUtils.get_db_connect()
        query = "select * from restaurants.order where table_number_id={0}  and generate_bill  is False ; ".format(
            table.id)

        # query = """
        #     SELECT c.items_id, c.quantity, oi.quantity AS delivered_quantity, (c.quantity - oi.quantity) AS quantity_difference
        #     FROM cart c
        #     LEFT JOIN order_Items oi ON c.orderid_id = oi.orderid_id AND c.items_id = oi.item_id_id
        #     JOIN `order` o ON c.orderid_id = o.id
        #     WHERE o.order_deliverd = 0 AND o.generate_bill = 0 table_number_id={0} ;
        #     """
        # print("query", query)
        get_existing_data = cursor.execute(query)
        rows = cursor.fetchall()
        data_list = []
        print("row", rows)
        for row in rows:
            data_list.append(row)
            print(row)

        cart_detail = None

        if len(data_list):

            cart_detail = Cart.objects.filter(table_number=table, orderid__generate_bill=False) | Cart.objects.filter(
                table_number=table, orderid__generate_bill=None)

            # cart_detail.extend(cart_detail_2)
            print("Order already exist")
        else:
            cart_detail = Cart.objects.filter(table_number=table, orderid_id__isnull=True)
            print("Order not exist")

        # cart_detail = Cart.objects.filter(table_number=table, orderid_id__isnull=True)
        # cart_detail = Cart.objects.filter(table_number=table, orderid__generate_bill=False)
        print("cart_detail count", cart_detail)
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
        print("inside  cart api post  ")
        table_name = request.data.get('table_name')  # Get the value of 'table_name'
        item_id = request.data.get('item_id')
        print("item_id", item_id)


        table = Owner_Utility.objects.get(table_number=table_name)
        owner_utility = Owner_Utility.objects.get(table_number=table_name)  # Assuming table_name is the primary key
        print("owner_utility", owner_utility)
        cursor, connection = DBUtils.get_db_connect()
        query = "select * from restaurants.order o join order_Items ot on (ot.orderid_id=o.id) where table_number_id={0}  and generate_bill  is False and ot.item_id_id = {1}; ".format(
            owner_utility.id,item_id)
        print("query", query)
        return_data = DBUtils.get_table_data(query, cursor)

        print("return_data", return_data)

        if  len(return_data):
            cart_items = Cart.objects.filter(table_number_id=table, items=item_id,
                                             cart_created=True,orderid__generate_bill=False).first()


            cart_item = cart_items  # Assuming there's only one item per table
            cart_item.quantity += 1
            cart_item.save()
            print("updated")
        else:
            cart_created = Cart.objects.filter(table_number=table, items=item_id, orderid__order_place=False,cart_created=False,orderid__generate_bill=True).first()
            print("cart_created", cart_created)

            if cart_created is None:
                print("Inside create new one for first time")
                table_number = Owner_Utility.objects.get(table_number=table_name)
                print("table_number", table_number)
                item = Items.objects.get(id=item_id)
                print("item_id", item_id)

                Cart.objects.create(table_number=table_number, items=item, cart_created=True)


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
            table = Owner_Utility.objects.get(table_number=table_number)
            print("table_number", table)

            cart_item = Cart.objects.filter(table_number=table, items=item_id,orderid=None).first()

            # Decrease the quantity by 1 if it's greater than 1
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

            return HttpResponse("Order item deleted successfully.")

        except Cart.DoesNotExist:
            return HttpResponseBadRequest("Order item not found.")

    def patch(self, request):

        try:
            print("cart patch request", request.data)
            print("cart patch request", request.data.get)
            item_id =  request.data.get('item_id')
            print("item_id", item_id)
            table_number = request.data.get('table_name')
            print("table_number",table_number)
            table = Owner_Utility.objects.get(table_number=table_number)
            print("table", table)
            # cart_items = Cart.objects.filter(table_number_id=table, items=item_id, cart_created=True, orderid__generate_bill=None).first()
            cart_items = Cart.objects.filter(
                Q(table_number_id=table, items=item_id, cart_created=True, orderid__generate_bill=None) |
                Q(table_number_id=table, items=item_id, cart_created=True, orderid__generate_bill=0)
            ).first()
            print("cart_items", cart_items)
            # cursor, connection = DBUtils.get_db_connect()
            # query = "select * from cart where table_number_id={0} and items_id={1} and orderid_id  is null  and cart_created=True ".format(table.id,item_id)
            # print("query", query)
            # get_existing_data = cursor.execute(query)
            # rows = cursor.fetchall()
            # data_list = []
            # print("row", rows)
            # for row in rows:
            #     data_list.append(row)
            #     print(row)

            if cart_items:
                print("Inside if ")
                cart_item = cart_items  # Assuming there's only one item per table
                cart_item.quantity += 1
                cart_item.save()
                print("updated")
            return JsonResponse({'message': 'Cart quantity updated successfully'})
        except Cart.DoesNotExist:
                return JsonResponse({'error': 'Cart not found'}, status=404)


