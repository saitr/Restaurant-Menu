# # Import the following modules
from pushbullet import PushBullet
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import time
from decouple import config
import requests

# Get the access token from Pushbullet.com
# access_token = "access_token "
# # Taking input from the user
# data = input('Enter the title: ')
# # Taking large text input from the user
# account_sid = config('pushbullot_notification_accesstoken')
# text = textarea(
#
#     "Text", rows=3, placeholder="Send bill for this table",
#
#     required=True)
#
# # Get the instance using the access token
#
# pb = PushBullet(access_token)
#
# # Send the data by passing the main title
#
# # and text to be send
#
# push = pb.push_note(data, text)
#
# # Put a success message after sending
#
# # the notification
# put_success("Message sent successfully...")
# # Sleep for 3 seconds
# time.sleep(3)
# # Clear the screen
# clear()
# # Give the pop at last
# toast("Thanks for Using :)")
# # hold the session until the whole work finishes
# hold()
#
# *******************
# import time
# import webbrowser
# from plyer import notification
#
# if __name__ == "__main__":
#     while True:
#         notification.notify(
#             title="ALERT!",
#             message="Take a break",
#             timeout=100
#         )
#         # Open the URL when the notification is displayed
#         webbrowser.open("http://127.0.0.1:8000/admin_view_page?csrfmiddlewaretoken=VeAhM0c3WANifdUQQ5dQNB1mqq0pHmFDLarhp1Zn9nBhIKlxVCjDhZFB9cfHug1y&phone_number=6361233478&password=100")
#         time.sleep(3600)


# *****************

#
# def admin_view_api(request):
#     # Process the data or perform any necessary operations
#
#     # Send a Pushbullet notification
#     send_pushbullet_notification(
#         title="New Admin View",
#         message="A new admin view has been accessed.",
#         url="http://127.0.0.1/admin_view_page"
#     )


# def send_pushbullet_notification(title, message, endpoint):
#     api_key = config('pushbullot_notification_accesstoken')
#     pb = pushbullet.Pushbullet(api_key)
#     push = pb.push_note(title, message)
#     push = pb.push_note(title, message, device=endpoint)
#     return push

# *****************************
# def send_pushbullet_notification(title, message, endpoint):
#     api_key = config('pushbullot_notification_accesstoken')
#     pb = pushbullet.Pushbullet(api_key)
#
#
#
#     try:
#             devices = pb.devices
#             print([device.nickname for device in devices])
#             device = next((d for d in devices if d.nickname.strip() == endpoint.strip()), None)
#             if device:
#                 push = pb.push_note(title, message, device=device.device_iden)
#                 return push
#             else:
#                 raise ValueError("Invalid endpoint provided")
#
#     except InvalidKeyError as e:
#         raise ValueError("Invalid Pushbullet API key") from e
#
# ****************
# def send_pushbullet_notification(title, message, endpoint):
#     api_key = config('pushbullot_notification_accesstoken')
#     pb = pushbullet.Pushbullet(api_key)
#     push = pb.push_note(title, message)
#     push = pb.push_note(title, message, device=endpoint)
#     return push
# if __name__ == "__main__":
#
#
#     url = 'http://127.0.0.1:8000/admin_view_page'
#     params = {
#         'csrfmiddlewaretoken': 'VeAhM0c3WANifdUQQ5dQNB1mqq0pHmFDLarhp1Zn9nBhIKlxVCjDhZFB9cfHug1y',
#         'phone_number': '6361233478',
#         'password': '100'
#     }
#     send_pushbullet_notification(
#                 title="New Admin View",
#                 message="A new admin view has been accessed.",
#                 url="http://127.0.0.1/admin_view_page"
#             )
#     response = requests.get(url, params=params)
#
#     # Check the response status code
#     if response.status_code == 200:
#         print('Notification sent successfully.')
#     else:
#         print('Failed to send notification.')
#
#
# *****************


import time
import webbrowser
from pushbullet import Pushbullet
from django.http import request
import pushbullet
from pushbullet.errors import InvalidKeyError


# Initialize the Pushbullet API with your API key
pb = Pushbullet("o.3NLZWA8Z2JyU2PgSVa959EEwcDrlrhN0")

def send_pushbullet_notification(title, message, url):
    push = pb.push_note(
        title=title,
        body=message,
        url='http://127.0.0.1:8000/admin_view_page?csrfmiddlewaretoken=VeAhM0c3WANifdUQQ5dQNB1mqq0pHmFDLarhp1Zn9nBhIKlxVCjDhZFB9cfHug1y&phone_number=6361233478&password=100'
    )




    # admin_view_api(request)

# from django.contrib import messages
# from django.shortcuts import redirect
#
# def first_view(request):
#     # Process the data or perform any necessary operations
#
#     # Add a notification message
#     messages.info(request, 'Notification message')
#
#     # Redirect to the second URL
#     return redirect('second_url')
