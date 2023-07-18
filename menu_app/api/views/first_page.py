from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect

import logging


LOGGER = logging.getLogger(__name__)

# Item api
class FirstPageAPIList(APIView):

    def get(self,request,variant):
        print("Inside  get first page",variant)
        table_name = variant
        print("table_name", table_name)
        context = {"table_name": table_name}
        print("context", context)

        return render(request, 'room_list.html', context)



