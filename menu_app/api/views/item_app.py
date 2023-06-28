from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import Items
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
        print("inside bus get", request.query_params)

        # print("from request", request.user.email)
        get_item = Items.objects.all()
        print("get_item", get_item)
        return_list = []
        for data in get_item:
            return_dict = {'category':data.category,
                           'itemName': data.itemName,
                           'itemPrice' : data.itemPrice,
                           'item_image': data.item_image,
                           'created_at':data.created_at,
                           'updated_at' : data.updated_at}
            return_list.append(return_dict)
        print("return_list", return_list)


        # return_status = status.HTTP_200_OK
        return render(return_list, 'signin.html')
        # return Response(data = return_list , status=return_status)