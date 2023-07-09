from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from ...models import CustomUser, Cart, Order_Items, Order,Owner_Utility
from ...serializers import OrderSerializer
from django.shortcuts import render, redirect
from menu_app.api.views.utils.database_helper import DBUtils
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate

class OrderApiView(APIView):
    def get(self,request):

        print("INSIDE GET OF ORDER ITEM for chef",request.query_params)
        password = request.query_params['password']
        phone_number = request.query_params['phone_number']
        user = authenticate(request, username=phone_number, password=password)
        if user is None:
            # Invalid credentials
            # Handle the error condition (e.g., return an error response)
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        else:
            # CustomUser.objects.get()
            cart_items = Cart.objects.filter(orderid__order_deliverd=False)

            return_list = []
            order_dict = {}

            for item in cart_items:
                order_id = item.orderid.id
                print("order_id *************", order_id)

                if order_id not in order_dict:
                    order_dict[order_id] = []

                item_data = {
                    "item_name": item.items.itemName,
                    "table_name": item.table_number.table_number,
                    "item": item.items,
                    "quantity": item.quantity
                }

                order_dict[order_id].append(item_data)

            # Convert order_dict into a list of dictionaries
            for order_id, items in order_dict.items():
                return_dict = {
                    order_id: items
                }
                return_list.append(return_dict)

            print(return_list)

            context = {
                'return_list': return_list
            }
            print("context", context)
            return render(request, 'chef.html', context)

    def post(self, request):
        print("Inside api OrderApiView post", request.data)
        table_name = request.data.get('table_name')
        print("table_name", table_name)
        owner_utility = Owner_Utility.objects.get(pk=table_name)  # Assuming table_name is the primary key
        print("owner_utility", owner_utility)
        # Step 1: Create an Order object
        order = Order.objects.create(table_number=owner_utility, total_price=0)
        print("order", order)


        # Step 2: Retrieve the items from the cart and create Order_Items
        order_items = []
        total_price = 0
        cursor, connection = DBUtils.get_db_connect()
        try:
            cart_items = Cart.objects.filter(table_number=table_name)

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
                                         item_id=item, orderid=order)
                order_items.append(order_item)
                total_price += order_item_price

                Cart.objects.filter(id=cart_item.id).update(orderid=order_item.orderid.id)

        except Cart.DoesNotExist:
            return JsonResponse({'message': 'Cart is empty'}, status=400)

        # Step 3: Save the order and order items
        order.total_price = total_price
        order.save()

        for order_item in order_items:
            order_item.save()
        context = {'table_name': table_name}
        return render(request, 'sign_up.html',context)

    def patch(self, request):
        print("Inside patch ********************************",request.data)

        try:
            data_dict = {"order_deliverd": True}
            order_id = request.data.get('order_id')
            print("Inside ***", order_id)
            previous_record = Order.objects.get(id=order_id)
            serializer = OrderSerializer(
                previous_record,
                data=data_dict,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                print("updated")
                return Response({'message': 'Order updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({'message': 'Order does not exist'}, status=status.HTTP_404_NOT_FOUND)