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
class AdminLoginDetailAPIList(APIView):

    def get(self,request):
        print("Inside admin login get")
        return render(request, 'admin_login.html')
        # return render(request, 'download_bill.html')
        # return render(request, 'room_list.html')
        # return render(request, 'new.html')

