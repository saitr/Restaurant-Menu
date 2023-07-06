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

from django.views import View

from django.shortcuts import render
from django.views import View
from django.contrib.auth.hashers import make_password

from .utils.database_helper import DBUtils
from rest_framework.authentication import SessionAuthentication


class VerifyOTPView(View):

    def get(self, request):
        print("Inside get")
        phone_number = request.session.get('phone_number')
        password = request.session.get('password')

        print("phone_number and password", phone_number, password)
        # if phone_number:
        #     # Send OTP when accessing the verification page via GET request
        #     print("Inside get phone number")
        #     verification_status, otp = send_otp_to_user(phone_number)
        #     if verification_status:
        #         print("Inside 1")
        #         # Store the OTP in the session for verification later
        #         request.session['otp'] = otp
        #         return render(request, 'verify_otp.html', {'phone_number': phone_number})
        #     else:
        #         print("Inside 2")
        #         # Handle the case where OTP sending failed
        #         return render(request, 'sign_up.html', {'error': 'Failed to send OTP. Please try again.'})
        # else:
        #     print("i AM HEAR")
            # Handle the case where phone number is not available in the session
        return render(request, 'sign_up.html', {"phone_number": phone_number,
                                                "password": password})


    def post(self, request):
        print("inside post USER_API")
        phone_number = request.POST.get('phone_number')
        print("phone_number", phone_number)

        if phone_number:
            user_dict = {}

            user_dict["phone_number"] = phone_number
            user_dict["password"] = make_password(request.POST.get('password'))
            cursor, connection = DBUtils.get_db_connect()
            query = "select * from  CustomUser where phone_number={0};".format(phone_number)
            get_existing_number = cursor.execute(query)
            rows = cursor.fetchall()
            data_list = []
            for row in rows:
                data_list.append(row)
                print(row)

            # get_existing_number = CustomUser.objects.get(phone_number=phone_number)
            # print("get_existing_number", get_existing_number)
            if len(data_list) == 0:
                print("create entry in database")
                CustomUser.objects.get_or_create(**user_dict)
            else:
                print("dont create")
            verification_status = send_otp_to_user(phone_number)
            print("verification_status", verification_status)

             # Handle the case where OTP sending failed
            return render(request, 'new.html', {'error': 'Failed to send OTP. Please try again.'})
        else:

            # Handle the case where phone number is not provided
            return render(request, 'new.html', {'error': 'Please enter a valid phone number.'})