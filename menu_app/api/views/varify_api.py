
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ...models import CustomUser
from ...serializers import CustomUserSerializer
from .utils.send_otp import send_otp_to_user, verify_otp
from django.shortcuts import render

import os



class ValidateOTPView(APIView):


    def post(self, request):
        print("Inside post verify api", request.POST.get)
        phone_number = request.POST.get('phone_number')
        entered_otp = request.POST.get('otp')
        print("phone_number", phone_number)
        print("entered_otp", entered_otp)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurants.settings.base")

        if entered_otp:
            # If OTP is provided, verify it
            verification_status = verify_otp(phone_number, entered_otp)
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
                print("updated")
                return redirect(request, 'home.html', {'error': 'Failed to send OTP. Please try again.'})

            else:
                # Handle the case where OTP verification failed
                return render(request, 'verify_otp.html',
                              {'phone_number': phone_number, 'error': 'Invalid OTP. Please try again.'})

        else:print("Invalid credential")