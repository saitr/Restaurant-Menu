from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import Owner_Utility


class Owner_UtilityView(APIView):

    def get(self, request, pk):
        try:
            instance = Owner_Utility.objects.get(pk=pk)
            # Perform any necessary actions for GET requests
            return Response(status=status.HTTP_200_OK)
        except Owner_Utility.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, pk):
        try:
            instance = Owner_Utility.objects.get(pk=pk)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Owner_Utility.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
