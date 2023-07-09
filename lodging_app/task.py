from restaurants.celery import app
from django.core.mail import send_mail

@app.task
def send_mail_async(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)
