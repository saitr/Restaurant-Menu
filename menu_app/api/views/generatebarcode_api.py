# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from ...models import Owner_Utility

class GenerateBarcodeView(APIView):
    def get(self, request, format=None):
        barcode = request.GET.get('barcode', None)
        print("barcode", barcode)
        if barcode is None:
            return Response({'error': 'Barcode parameter missing.'}, status=400)

        try:
            table = Owner_Utility.objects.get(barcode=barcode)
            api_link = f'http://127.0.0.1:8000/category_api/{Owner_Utility.table_number}/'
            return Response({'table_number': table.table_number, 'api_link': api_link})
        except Owner_Utility.DoesNotExist:
            return Response({'error': 'Table not found.'}, status=404)
