from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import Items,Categories
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
        print("inside item get", request.query_params['category'])
        try:
            selected_category = Categories.objects.get(categoryName=request.query_params['category'])
            get_item = Items.objects.filter(category=selected_category)
        except Categories.DoesNotExist:
            get_item = []  #


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

        context = {
            'return_list': return_list
        }

        return render(request, 'item.html', context)

