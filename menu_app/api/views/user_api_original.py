import logging
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import render, redirect
from ...models import User
import os
from ...serializers import CustomUserSerializer
from django.core import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404
import json
from .utils.database_helper import DBUtils

from twilio.rest import Client
from restaurants.settings.base import *
from .utils.send_otp import  send_otp_to_user,verify_otp




# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


# Item api
class UserAPIList(APIView):

    def post(self, request):
        print("inside  user api", request.data)

        user_dict = {}
        # if 'phone_number' in request.data:

        user_dict["phone_number"] = request.data['phone_number']

        verified_number = config('VERIFIED_NUMBER')
        verification_status = send_otp_to_user(verified_number)
        verify_otp(verified_number, verification_status)
        User.objects.create(**user_dict)




        return_status = status.HTTP_200_OK
        return Response(data=user_dict,
                        status=return_status)

