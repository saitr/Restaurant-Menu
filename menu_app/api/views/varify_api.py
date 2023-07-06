# Assuming you have already defined send_otp_to_user and verify_otp functions in your .utils.send_otp module
from django.shortcuts import render, redirect
from restaurants.settings.base import *
from .utils.send_otp import send_otp_to_user, verify_otp
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ...models import CustomUser
from ...serializers import CustomUserSerializer
# views.py
from django.contrib.auth import authenticate
from django.views import View
from .utils.send_otp import send_otp_to_user, verify_otp
from django.shortcuts import render
from django.views import View
from .utils.database_helper import DBUtils
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from menu_app.api.views.utils.database_helper import DBUtils
import os
import requests


class ValidateOTPView(View):


    def post(self, request):
        print("Inside post verify api")
        phone_number = request.POST.get('phone_number')
        entered_otp = request.POST.get('otp')
        print("phone_number", phone_number)
        print("entered_otp", entered_otp)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurants.settings.base")
        user = authenticate(phone_number=phone_number, password=(request.POST.get('password')))
        print("user athentication")
        if user is not None:
            request.session['phone_number'] = phone_number
            print("Sessiondata",request.session['phone_number'])
            if entered_otp:
                # If OTP is provided, verify it
                verification_status = verify_otp(phone_number, entered_otp)
                if verification_status:

                    # cursor, connection = DBUtils.get_db_connect()
                    # query = "select * from  CustomUser where phone_number={0};".format(phone_number)
                    # cursor.execute(query)
                    #
                    # data_list = []
                    # rows = cursor.fetchall()
                    # for row in rows:
                    #     data_list.append(row)
                    #     print(row)
                    # del request.session['phone_number']
                    # print("data_list", data_list)

                    # if len(data_list) != 0:
                        previous_record = CustomUser.objects.get(phone_number=phone_number)
                        print("Updating")
                        data_dict = {"is_verified": True}

                        serializer = CustomUserSerializer(
                            previous_record,
                            data=data_dict,
                            partial=True
                        )
                        if serializer.is_valid(raise_exception=True):
                           serializer.save()
                        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurants.settings.base")

                # If the OTP is successfully verified, redirect to the category API view
                #         return redirect('category_api')
                        response = requests.get('http://127.0.0.1:8000/category_api/')
                        # print("response", response.json())
                        if response.status_code == 200:
                            print("Inside")
                            # return render(request, 'dummy_category.html')
                            return render(request, 'dummy_category.html', {'error': 'Failed to send OTP. Please try again.'})
                        else:
                            # Handle the case where the request to the category API failed
                            # You may want to return an error message or redirect to some other page
                            return render(request, 'error_page.html', {'error': 'Failed to fetch categories.'})

                    #     category_api_url = 'http://127.0.0.1:8000/category_api/'  # Replace this with the actual URL of CategoryAPIList
                    #     response = requests.get(category_api_url)
                    #     print("response", response)
                    #
                    #     if response.status_code == 200:
                    #         return render(request, 'category.html', {'return_list': response.json()})
                    # Replace 'category-api-url' with the actual URL of your category API view

                else:
                    # Handle the case where OTP verification failed
                    return render(request, 'verify_otp.html',
                                  {'phone_number': phone_number, 'error': 'Invalid OTP. Please try again.'})

        else:print("Invalid credential")