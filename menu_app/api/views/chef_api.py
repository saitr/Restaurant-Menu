from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import Cart,Items
import os
from ...serializers import CartSerializer
from django.core import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404
import json
import logging
from .utils.database_helper import DBUtils
from django.http import HttpResponseRedirect

LOGGER = logging.getLogger(__name__)

# Item api
class ChefAPIList(APIView):

    def get(self,request):
        print("Inside chef get")
        return render(request, 'login.html')


    def post(self,request):
        print("inside post chef add ")
        request.data("")

