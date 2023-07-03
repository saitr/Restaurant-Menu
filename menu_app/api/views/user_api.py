# Assuming you have already defined send_otp_to_user and verify_otp functions in your .utils.send_otp module
from django.shortcuts import render, redirect
from restaurants.settings.base import *
from .utils.send_otp import send_otp_to_user, verify_otp
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ...models import CustomUser
# ...
# views.py

from django.views import View
from .utils.send_otp import send_otp_to_user, verify_otp
from django.shortcuts import render
from django.views import View


class VerifyOTPView(View):

    def get(self, request):
        print("Inside get")
        phone_number = request.session.get('phone_number')
        print("phone_number", phone_number)
        if phone_number:
            # Send OTP when accessing the verification page via GET request
            print("Inside get phone number")
            verification_status, otp = send_otp_to_user(phone_number)
            if verification_status:
                print("Inside 1")
                # Store the OTP in the session for verification later
                request.session['otp'] = otp
                return render(request, 'verify_otp.html', {'phone_number': phone_number})
            else:
                print("Inside 2")
                # Handle the case where OTP sending failed
                return render(request, 'sign_up.html', {'error': 'Failed to send OTP. Please try again.'})
        else:
            print("i AM HEAR")
            # Handle the case where phone number is not available in the session
            return render(request, 'sign_up.html', {'error': 'Phone number not found in session. Please try again.'})


    def post(self, request):
        print("inside post")
        phone_number = request.POST.get('phone_number')
        entered_otp = request.POST.get('otp')
        print("phone_number", phone_number)

        if phone_number:
            if entered_otp:
                # If OTP is provided, verify it
                verification_status = verify_otp(phone_number, entered_otp)
                if verification_status:
                    # OTP verified successfully, do something
                    # For example, create the user account with the provided phone number
                    # You can also clear the session variables here if needed
                    del request.session['phone_number']

                    # Add your logic here to create the user account or perform any other action

                    # If the OTP is successfully verified, redirect to the category API view
                    return redirect(
                        'category_api')  # Replace 'category-api-url' with the actual URL of your category API view

                else:
                    # Handle the case where OTP verification failed
                    return render(request, 'verify_otp.html',
                                  {'phone_number': phone_number, 'error': 'Invalid OTP. Please try again.'})
            else:
                # If OTP is not provided, send OTP
                verification_status = send_otp_to_user(phone_number)
                if verification_status == 'pending':
                    print("Inside 1")
                    # Store the OTP in the session for verification later
                    request.session['phone_number'] = phone_number
                    return render(request, 'verify_otp.html', {'phone_number': phone_number})
                else:
                    print("Inside 2")
                    # Handle the case where OTP sending failed
                    return render(request, 'sign_up.html', {'error': 'Failed to send OTP. Please try again.'})
        else:
            # Handle the case where phone number is not provided
            return render(request, 'verify_otp.html', {'error': 'Please enter a valid phone number.'})
