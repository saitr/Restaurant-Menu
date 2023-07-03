from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import Categories
import os
from ...serializers import ItemsSerializer
from django.core import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404
import json
import logging

LOGGER = logging.getLogger(__name__)

# Item api
class CategoryAPIList(APIView):

    def get(self, request):
        print("inside  category_api", request.query_params)

        # print("from request", request.user.email)
        get_item = Categories.objects.all()
        print("get_item", get_item)
        return_list = []
        for data in get_item:
            return_dict = {'categoryName':data.categoryName}

            return_list.append(return_dict)
        print("return_list", return_list)

        context = {
            'return_list': return_list
        }

        return render(request, 'category.html', context)

