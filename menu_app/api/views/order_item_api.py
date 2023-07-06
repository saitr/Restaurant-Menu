from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from ...models import CustomUser, Cart, Order_Items, Order,Owner_Utility
from ...serializers import OrderSerializer
from django.shortcuts import render, redirect

class OrderApiView(APIView):
    def get(self,request):
        print("request.query_params",request.query_params)
        cart_items = Cart.objects.all()
        # Cart :- quantity,items,table_number
        # Order_Items: - quantity, order_item_price, item_id, orderid,
        # Items:- category, itemName, itemPrice, item_image, created_at, updated_at
        return_list = []
        for item in cart_items:
            print("cart_item.id", item.id)
            # Assuming you have the cart item ID
            return_dict = {
            "item_name": item.items.itemName,
            "table_name" : item.table_name,
            "item" : item.items,
            "quantity" : item.quantity
            }
            return_list.append(return_dict)

        context = {
            'return_list': return_list
        }
        print("context", context)
        return render(request, 'chef.html', context)

    def post(self, request):
        print("Inside api OrderApiView", request.data)
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

        try:
            cart_items = Cart.objects.filter(table_number=table_name)

            for cart_item in cart_items:
                print("cart_item.id", cart_item.id)
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
        except Cart.DoesNotExist:
            return JsonResponse({'message': 'Cart is empty'}, status=400)

        # Step 3: Save the order and order items
        order.total_price = total_price
        order.save()

        for order_item in order_items:
            order_item.save()

        return JsonResponse({'message': 'Order created successfully'}, status=200)
