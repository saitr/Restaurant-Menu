from django.core.serializers.json import DjangoJSONEncoder
from ....models import Items

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Items):
            # Customize the serialization of the Items object
            return {
                'item_name': obj.itemName,
                # Add more fields as needed
            }
        return super().default(obj)
