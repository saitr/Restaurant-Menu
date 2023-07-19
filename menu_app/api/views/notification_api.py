from django.http import HttpResponse
from django.views.generic import View
import json
import time
import webbrowser
from pushbullet import Pushbullet
from django.http import request
from decouple import config

import pushbullet

class NotificationAPIList(View):

    def get(self, request):
        # ... Existing code ...
        print("inside get notification",request.GET.get)
        # Send SSE notification to the browser
        order_id = request.GET.get('order_id')
        print("order_id", order_id)


        title = "Generate Bill"
        message = "From chef"
        token = config('pushbullot_notification_accesstoken')
        pb = pushbullet.Pushbullet(token)
        message = "Please generate bill for order id " +  order_id
        message_str = json.dumps(message)
        push = pb.push_note(title=title, body=message_str)
        return HttpResponse('Notification sent successfully')

