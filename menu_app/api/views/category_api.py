from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import Categories
from django.http import JsonResponse
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

    def get(self, request,variant):
        print("inside  category_api", request.query_params)

        # print("from request", request.user.email)
        get_item = Categories.objects.all()
        print("get_item", get_item)
        return_list = []
        for data in get_item:
            return_dict = {'categoryName':data.categoryName,
                           'category_img': data.category_img,'table_number': variant}

            return_list.append(return_dict)

        context = {
            'return_list': return_list
        }
        print("context", context)
        # return Response(context, status=status.HTTP_200_OK)
        return render(request, 'category.html', context)

