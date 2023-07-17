from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import Owner_Utility
from django.shortcuts import render
import json

class Owner_UtilityView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            try:
                instance = Owner_Utility.objects.get(pk=pk)
                # Perform any necessary actions for GET requests with a specific pk
                return Response(status=status.HTTP_200_OK)
            except Owner_Utility.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            table_data_set = []
            queryset = Owner_Utility.objects.all()
            for data in queryset:
                initial_dict = {"table_number":data.table_number}
                table_data_set.append(initial_dict)

            context = {'table_data_set': table_data_set}
            print("context", context)
            return render(request, 'owner_utility.html', context)

    def delete(self, request, pk):
        try:
            instance = Owner_Utility.objects.get(pk=pk)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Owner_Utility.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
