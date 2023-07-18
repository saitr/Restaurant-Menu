from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import Cart,Items,CustomUser
import os
from ...serializers import CartSerializer
from django.core import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404
import json
import logging
from .utils.database_helper import DBUtils
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password,check_password
from rest_framework.permissions import IsAdminUser
from django.contrib import messages
from django.db import IntegrityError

LOGGER = logging.getLogger(__name__)

# Item api
class AddChefAPIList(APIView):

    def get(self,request):
        print("Inside add chef get")
        permission_classes = [IsAdminUser]
        print("INSIDE GET OF ORDER ITEM for Admin", request.query_params)
        print("INSIDE GET OF ORDER ITEM for Admin", request)
        admin_password = request.query_params['password']
        admin_phone_number = request.query_params['phone_number']

        try:
            user = CustomUser.objects.get(phone_number=admin_phone_number)
            print("User", user.password)
            print("User", admin_password)
            print("super", user.is_superuser)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None and check_password(admin_password, user.password) and user.is_superuser:
            return render(request, 'add_chef.html')
        else:
            print("invalid")
            messages.error(request, 'Invalid credentials')  # Add error message to Django messages framework

        # Pass the error message to the template
            return render(request, 'admin_login.html', {'error_message': 'Invalid credentials'})


    def post(self,request):
            try:
                print("INSIDE post OF ORDER ITEM for Admin", request.query_params)
                print("INSIDE post OF ORDER ITEM for Admin", request)
                print("valid")
                print("inside post chef add ",request.data)
                print("inside post chef add ",request.data['user_name'])
                user_name = request.data['user_name']
                phone_number = request.data['phone_number']
                password = request.data['password']
                email_id = request.data['email_id']
                # Hash the password
                hashed_password = make_password(password)

                user = CustomUser.objects.create(
                    username=user_name,
                    phone_number=phone_number,
                    password=hashed_password,
                    email=email_id
                )
                return render(request, 'add_chef.html', {'message': 'Chef added successfully'})
            except IntegrityError:
                error_message = 'Phone number already exists. Please choose a different phone number.'
                return render(request, 'add_chef.html', {'error_message': error_message})
            # Return a response

