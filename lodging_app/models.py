from django.db import models
from menu_app.models import *
from django.contrib.auth.models import AbstractUser

from rest_framework.authtoken.models import Token
from cloudinary.models import CloudinaryField
import secrets
# Lodging Class 


# class Lodge(models.Model):
#     Number_Of_People = (
#         ("1", "1"),
#         ("2", "2"),
#         ("3", "3"),
#         ("4", "4"),
#     )
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lodges')
#     room_chosen = models.ForeignKey(Owner_Utility, on_delete=models.CASCADE)
#     from_date = models.DateTimeField(blank=False, null=False)
#     to_date = models.DateTimeField(blank=False, null=False)
#     check_in = models.BooleanField(default=False)
#     check_out = models.BooleanField(default=False)
#     number_of_people = models.CharField(choices=Number_Of_People, max_length=4)
#     check_in_date_time = models.DateTimeField(blank=True, null=True)
#     check_out_date_time = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         db_table = 'Lodging'


class Lodge(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lodges')
    room_chosen = models.ForeignKey(Owner_Utility, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    number_of_people = models.IntegerField()
    check_in = models.BooleanField(default=False)
    check_out = models.BooleanField(default=False)
    check_in_date_time = models.DateTimeField(null=True, blank=True)
    check_out_date_time = models.DateTimeField(null=True, blank=True)


class Invoice(models.Model):
    lodge = models.ForeignKey(Lodge, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    paid= models.BooleanField(default=False)
