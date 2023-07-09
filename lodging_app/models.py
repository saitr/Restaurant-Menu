from django.db import models
from menu_app.models import *
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from rest_framework.authtoken.models import Token
from cloudinary.models import CloudinaryField
import secrets
# Lodging Class 


class Lodge(models.Model):
    Number_Of_People = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lodges')
    room_chosen = models.ForeignKey(Owner_Utility, on_delete=models.CASCADE)
    from_date = models.DateTimeField(blank=False, null=False)
    to_date = models.DateTimeField(blank=False, null=False)
    check_in = models.BooleanField(default=False)
    check_out = models.BooleanField(default=False)
    number_of_people = models.CharField(choices=Number_Of_People, max_length=4)
    check_in_date_time = models.DateTimeField(blank=True, null=True)
    check_out_date_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'Lodging'