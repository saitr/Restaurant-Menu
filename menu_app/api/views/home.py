from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect

class HomeAPIList(APIView):

    def get(self,request):

        return render(request, 'home.html')
