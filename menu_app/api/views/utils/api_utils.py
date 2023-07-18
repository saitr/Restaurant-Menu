from django.core.serializers.json import DjangoJSONEncoder
from ....models import Items
import pushbullet
from decouple import config


class CustomJSONEncoder(DjangoJSONEncoder):
    # def default(self, obj):
    #     if isinstance(obj, Items):
    #         # Customize the serialization of the Items object
    #         return {
    #             'item_name': obj.itemName,
    #             # Add more fields as needed
    #         }
    #     return super().default(obj)



    def send_pushbullet_notification(title, message, endpoint):
        api_key = config('pushbullot_notification_accesstoken')
        pb = pushbullet.Pushbullet(api_key)
        push = pb.push_note(title, message)
        push = pb.push_note(title, message, device=endpoint)
        return push

