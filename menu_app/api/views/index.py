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


class indexAPIList(APIView):

    def get(self, request,variant):
        print("Inside index get")


        return render(request, 'index.html', {"table_number": variant})


