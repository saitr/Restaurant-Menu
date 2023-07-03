from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import Cart
import os
from ...serializers import CartSerializer
from django.core import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404
import json
import logging
from .utils.database_helper import DBUtils


LOGGER = logging.getLogger(__name__)

# Item api
class CartAPIList(APIView):




    def post(self, request):
        print("inside  cart api", request.data)
        user_id = request.user
        print("user_id", user_id)
        post_set = {
        "userId" : request.data['userId'],
        "items" : request.data['items'],
        "quantity" : request.data['quantity']
        }
        self.db_utils_obj = DBUtils()
        self.db_utils_obj.set_serializer_object(
            model_serializer=CartSerializer,
            data_dict=post_set
        )

        return render(request, 'category.html')

