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
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
import json
from menu_app.api.views.utils import api_utils
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


class OrderApiView(APIView):
    def get(self,request):

        print("INSIDE GET OF ORDER ITEM for chef",request.query_params)
        password = request.query_params['password']
        phone_number = request.query_params['phone_number']
        hashed_password = make_password(password)
        # user = authenticate(request, username=phone_number, password=hashed_password)
        # print("user", user)
        user = CustomUser.objects.filter(phone_number=phone_number,is_chef=True).first()  # Assuming User is the user model you are using
        print("user", user)
        password_matched = check_password(password, user.password)

        if not password_matched:
            print("invalid")

            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
        else:
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
                        "order_id":item.orderid_id,
                        "order_deliverd":item.sub_order_id.order_deliverd
                    }
                list_item.append(item_data)

            order_dict = {}

            for item in list_item:
                print("****************************", item['order_id'])
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

            return render(request, 'chef.html', context)

    def post(self, request):
        print("Inside api OrderApiView post", request.data)
        table_name = request.data.get('table_name')
        print("table_name", table_name)

        owner_utility = Owner_Utility.objects.get(table_number=table_name)  # Assuming table_name is the primary key
        print("owner_utility", owner_utility)

        cursor, connection = DBUtils.get_db_connect()
        query = "select * from restaurants.order where table_number_id={0}  and generate_bill  is False ; ".format(owner_utility.id)
        print("query", query)
        get_existing_data = cursor.execute(query)
        rows = cursor.fetchall()
        data_list = []
        print("row", rows)
        for row in rows:
            data_list.append(row)
            print(row)
        if len(data_list):
            order_existing_check = Order.objects.get(table_number=owner_utility, generate_bill=False)
            print("order_existing_check", order_existing_check)
            print("already exist")
            order = order_existing_check
            if order_existing_check:
                # check suborder existence
                sub_order_exist = SubOrder.objects.filter(table_number=owner_utility,order_place=True).first()
                print("sub_order_exist", sub_order_exist)
                if sub_order_exist:
                    sub_order_exist = SubOrder.objects.create(table_number=owner_utility, total_price=0)
                    print("Create suborder", sub_order_exist)
                else:
                    sub_order_exist = SubOrder.objects.filter(table_number=owner_utility, order_place=False).first()
                    print("SubOrder already exist")

        else:
            # Step 1: Create an Order object
            print("Create order")
            order = Order.objects.create(table_number=owner_utility, total_price=0)
            print("Create an Order object", order)

            sub_order_exist = SubOrder.objects.create(table_number=owner_utility, total_price=0)
            print("Create suborder", sub_order_exist)


        # Step 2: Retrieve the items from the cart and create Order_Items
        order_items = []
        total_price = 0

        try:
            print("Inside try")
            cart_items = Cart.objects.filter(table_number=owner_utility,sub_order_id_id__isnull=True)
            print("cart_items", cart_items)

            for cart_item in cart_items:
                print("cart_item.id", cart_item)
               # Assuming you have the cart item ID
                item_price = cart_item.items.itemPrice
                print("item_price", item_price)
                item = cart_item.items
                quantity = cart_item.quantity

                # item_price = item.itemPrice
                order_item_price = quantity * item_price

                # Create an Order_Items object
                order_item = Order_Items.objects.create(quantity=quantity, order_item_price=order_item_price,
                                         item_id=item, orderid=order,sub_order_id_id=sub_order_exist.id)

                print("order_item",order_item)

                order_items.append(order_item)
                total_price += order_item_price

                Cart.objects.filter(id=cart_item.id,orderid_id__isnull=True).update(orderid=order_item.orderid.id,sub_order_id_id=order_item.sub_order_id_id)
                # print("updating cartid", order_item.orderid.id)
                # cart_item.orderid = order_item.orderid.id
                # cart_item.save()
                print("update",cart_item )
                print("update",cart_item.orderid )


        except Cart.DoesNotExist:
            return JsonResponse({'message': 'Cart is empty'}, status=400)

        # Step 3: Save the order and order items
        sub_order_exist.total_price = total_price
        sub_order_exist.order_place = True
        sub_order_exist.main_orderid_id = order
        sub_order_exist.save()

        for order_item in order_items:
            order_item.save()
        context = {'table_name': table_name}
        print("context", context)
        return render(request, 'sign_up.html',context)

    def patch(self, request):
        print("Inside patch ********************************",request.data)

        try:
            data_dict = {"order_deliverd": True}
            sub_order_id = request.data.get('subOrderId')
            print("Inside ***", sub_order_id)
            previous_record = SubOrder.objects.get(id=sub_order_id)
            serializer = SubOrderSerializer(
                previous_record,
                data=data_dict,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                print("updated")
                return Response({'message': 'Order updated successfully',
                                 'updated_sub_order_id': sub_order_id}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({'message': 'Order does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):

        print("inside delete sub order item", request.data)

        sub_order_id = request.data['subOrderId']
        order_id = request.data['order_id']

        print("sub_order_id", sub_order_id)

        try:

            sub_order_item = SubOrder.objects.filter(
                Q(id=sub_order_id,
                  order_deliverd=False)

            ).first()

            print("sub_order_item", sub_order_item)

            if sub_order_item:
                sub_order_item.delete()

            suborder_count = SubOrder.objects.filter(main_orderid_id=order_id).count()

            if suborder_count == 0:
                # No suborders found, delete the order
                print("delete order")
                Order.objects.filter(id=order_id).delete()

            return HttpResponse("Order item deleted successfully.")

        except Cart.DoesNotExist:
            return HttpResponseBadRequest("Order item not found.")
