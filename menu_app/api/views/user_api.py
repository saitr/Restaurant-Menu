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
# views.py

from django.views import View

from django.shortcuts import render
from django.views import View
from django.contrib.auth.hashers import make_password

from .utils.database_helper import DBUtils
from rest_framework.authentication import SessionAuthentication


class VerifyOTPView(APIView):

    def get(self, request):
        print("Inside get")
        phone_number = request.session.get('phone_number')

        return render(request, 'sign_up.html', {"phone_number": phone_number})


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



    def post(self, request):
        print("inside post USER_API", request.data )
        print("inside post USER_API", request )
        phone_number = request.POST.get('phone_number')
        print("phone_number", phone_number)
        table_name = request.POST.get('table_name')
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

            # get_existing_number = CustomUser.objects.get(phone_number=phone_number)
            # print("get_existing_number", get_existing_number)
            if len(data_list) == 0:
                print("create entry in database")
                CustomUser.objects.get_or_create(**user_dict)
            else:
                print("dont create")

            user = CustomUser.objects.get(phone_number=phone_number)
            print("user.is_verified", user.is_verified)
            if user.is_verified == False:
                verification_status = send_otp_to_user(phone_number)
                print("verification_status", verification_status)
                return render(request, 'new.html', {"phone_number": phone_number})
            else:
                # url = 'http://127.0.0.1:8000/items?category={0}&table_name={1}'.format(
                #     category_name['category__categoryName'], table_name)
                # # return redirect(url)
                print("url*************** else")
                url = ('http://127.0.0.1:8000/category_api/{0}/').format(table_name)
                print("url", url)
                return redirect(url)

                # print("customer already created and verify", request)
                # return render(request, 'home.html', {'error': 'Failed to send OTP. Please try again.'})

                # return render(request, 'home.html', {'error': 'Failed to send OTP. Please try again.'})

             # Handle the case where OTP sending failed

        if phone_number and entered_otp:
            # If OTP is provided, verify it
            verification_status = verify_otp(phone_number, entered_otp)
            print("verification_status", verification_status)
            if verification_status:

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
                    print("updated", request)
                    return JsonResponse({'success': True})  # Return a JSON response indicating success
                else:
                    return JsonResponse({'success': False})
                # return redirect((request.META.get('HTTP_REFERER', 'home')))
                # return JsonResponse({'message': 'OTP verification successful'})

        # print("out")
        return render(request, 'home.html', {'error': 'Failed to send OTP. Please try again.'})



            # else:
            #     # Handle the case where OTP verification failed
            #     return render(request, 'verify_otp.html',
            #                   {'phone_number': phone_number, 'error': 'Invalid OTP. Please try again.'})
