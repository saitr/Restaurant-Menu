# Assuming you have already defined send_otp_to_user and verify_otp functions in your .utils.send_otp module
from django.shortcuts import render, redirect
from restaurants.settings.base import *
from .utils.send_otp import send_otp_to_user, verify_otp
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ...models import CustomUser
from ...serializers import CustomUserSerializer
from django.http import JsonResponse
import random
import string
from django.http import HttpResponseRedirect
import requests
# views.py

from django.views import View

from django.shortcuts import render
from django.views import View
from django.contrib.auth.hashers import make_password

from .utils.database_helper import DBUtils
from rest_framework.authentication import SessionAuthentication


class VerifyOTPView(APIView):

    def get(self, request):
        print("Inside get user api",request)
        print("Inside get api",request.GET.get('table_name'))
        table_name = request.GET.get('table_name')
        print("table_name", table_name)
        phone_number = request.session.get('phone_number')

        return render(request, 'sign_up.html', {"phone_number": phone_number,
                                                "table_number": table_name})


    #
    # def post(self, request):
    #     print("inside post USER_API")
    #     phone_number = request.POST.get('phone_number')
    #     print("phone_number", phone_number)
    #
    #     if phone_number:
    #         user_dict = {}
    #
    #         user_dict["phone_number"] = phone_number
    #
    #         cursor, connection = DBUtils.get_db_connect()
    #         query = "select * from  CustomUser where phone_number={0};".format(phone_number)
    #         get_existing_number = cursor.execute(query)
    #         rows = cursor.fetchall()
    #         data_list = []
    #         for row in rows:
    #             data_list.append(row)
    #             print(row)
    #
    #         # get_existing_number = CustomUser.objects.get(phone_number=phone_number)
    #         # print("get_existing_number", get_existing_number)
    #         if len(data_list) == 0:
    #             print("create entry in database")
    #             CustomUser.objects.get_or_create(**user_dict)
    #         else:
    #             print("dont create")
    #
    #         user = CustomUser.objects.get(phone_number=phone_number)
    #         print("user.is_verified", user.is_verified)
    #         if user.is_verified == False:
    #             verification_status = send_otp_to_user(phone_number)
    #             print("verification_status", verification_status)
    #             return render(request, 'new.html', {"phone_number": phone_number})
    #         else:
    #             print("customer already created and verify")
    #             return render(request, 'home.html', {'error': 'Failed to send OTP. Please try again.'})
    #
    #          # Handle the case where OTP sending failed
    #
    #     else:
    #
    #         # Handle the case where phone number is not provided
    #         return render(request, 'new.html', {'error': 'Please enter a valid phone number.'})
    def generate_otp(self):
        length = 6
        characters = string.digits
        otp = ''.join(random.choice(characters) for _ in range(length))
        return otp


    def post(self, request):
        print("inside post USER_API", request.data )
        print("inside post USER_API", request )
        phone_number = request.POST.get('phone_number')
        print("phone_number", phone_number)
        table_name = request.POST.get('table_number')
        print("table_name", table_name)
        entered_otp = request.POST.get('otp')
        print("entered_otp", entered_otp)

        if phone_number and not entered_otp:
            user_dict = {}

            user_dict["phone_number"] = phone_number

            cursor, connection = DBUtils.get_db_connect()
            query = "select * from  CustomUser where phone_number={0};".format(phone_number)
            get_existing_number = cursor.execute(query)
            rows = cursor.fetchall()
            data_list = []
            for row in rows:
                data_list.append(row)
                print(row)


            if len(data_list) == 0:
                print("create entry in database")
                CustomUser.objects.get_or_create(**user_dict)
            else:
                print("dont create")

            user = CustomUser.objects.get(phone_number=phone_number)
            print("user.is_verified", user.is_verified)
            if user.is_verified == False:
                # verification_status = send_otp_to_user(phone_number)
                otp = self.generate_otp()
                print("otp", otp)
                user.otp = otp
                user.save()
                print("Saved otp")
                return render(request, 'new.html', {"phone_number": phone_number,"table_name": table_name})
            else:
                print("url*************** else")
                order_api_url = 'http://127.0.0.1:8000/order_api/'
                payload = {
                    'table_name': table_name,
                }
                response = requests.post(order_api_url, data=payload)
                if response.status_code == 200:
                    # Handle successful response from the order_api
                    # Redirect or perform any other necessary action
                    url = ('http://127.0.0.1:8000/category_api/{0}/').format(table_name)
                    return HttpResponseRedirect(url)
                else:
                    # Handle unsuccessful response from the order_api
                    return render('error_page.html')
                # url = ('http://127.0.0.1:8000/order_api/{0}/').format(table_name)
                # print("url", url)
                # return redirect(url)



        if phone_number and entered_otp:
            # If OTP is provided, verify it
            previous_record = CustomUser.objects.get(phone_number=phone_number)

            # verification_status = verify_otp(phone_number, entered_otp)
            # print("verification_status", verification_status)
            if entered_otp == previous_record.otp:


                print("verification_status  Updating")
                data_dict = {"is_verified": True}

                serializer = CustomUserSerializer(
                    previous_record,
                    data=data_dict,
                    partial=True
                )
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    print("updated", request)
                    response_data = {
                        'success': True,
                        'table_name': table_name
                    }
                    print("response_data", response_data)
                    return JsonResponse(response_data)  # Return a JSON response indicating success
                else:
                    return JsonResponse({'success': False})



        # return render(request, 'home.html', {'error': 'Failed to send OTP. Please try again.'})
        url = ('http://127.0.0.1:8000/category_api/{0}/').format(table_name)
        print("url", url)
        return redirect(url)


            # else:
            #     # Handle the case where OTP verification failed
            #     return render(request, 'verify_otp.html',
            #                   {'phone_number': phone_number, 'error': 'Invalid OTP. Please try again.'})
