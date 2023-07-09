from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
# from jsonfield import JSONField
from  cloudinary.models import CloudinaryField

# from menu_app.models import User
from lodging_app.managers import UserManager
from rest_framework.authtoken.models import Token
import secrets

import uuid
# from .manager import CustomUserManager

class User(AbstractUser):
    username = models.CharField(max_length=250,null=True,blank=True,unique=True)
    password = models.CharField(max_length=100,null=False,blank=False)
    phone_number = models.CharField(null=True,blank=True,max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField(max_length=250)
    jwt_token = models.CharField(max_length=250,unique=True,null=True)
    token = models.CharField(max_length=100,unique=True,null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    is_logged_in = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)
    display_picture = CloudinaryField('Display Picture',null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS =['username','phone_number']
    class Meta:
        db_table = 'User'
    
    # function to create a token 
    def save_token(self, *args, **kwargs):
        if not self.token:
            # generate new token if none exists
            self.token = secrets.token_urlsafe(32)

        super().save(*args, **kwargs)

    
    def update_token(self):
        self.token = None
        self.token_created = None
        self.token_expires = None
        self.save()


# class Categories(models.Model):
#     categoryName = models.CharField(max_length=255)

#     def __str__(self):
#         return self.categoryName

#     class Meta:
#         managed = True
#         db_table = 'categories'

# class Items(models.Model):
#     category = models.ForeignKey(Categories, on_delete=models.CASCADE)
#     itemName = models.CharField(max_length=255)
#     itemPrice = models.IntegerField()
#     item_image = CloudinaryField(blank=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.itemName

#     class Meta:
#         managed = True
#         db_table = 'items'


# class Cart(models.Model):
#     userId = models.ForeignKey(User, on_delete=models.CASCADE)
#     items = models.ForeignKey(Items, on_delete=models.CASCADE)
#     quantity = models.IntegerField()

#     def __str__(self):
#         return self.userId

#     class Meta:
#         managed = True
#         db_table = 'cart'


# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     table_number = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     total_price = models.IntegerField()

#     def __str__(self):
#         return self.table_number

#     class Meta:
#         managed = True
#         db_table = 'order'

# class Order_Items(models.Model):
#     quantity = models.IntegerField()
#     order_item_price = models.IntegerField()
#     item_id = models.ForeignKey(Items, on_delete=models.CASCADE)
#     orderid = models.ForeignKey(Order, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.item_id

#     class Meta:
#         managed = True
#         db_table = 'order_Items'

# class Lodge(models.Model):
#     userid = models.ForeignKey(User, on_delete=models.CASCADE)
#     room_number = models.IntegerField()
#     from_date = models.DateTimeField()
#     to_date = models.DateTimeField()
#     identity_proof = CloudinaryField(blank=False)
#     is_booked = models.BooleanField()
#     checkIn = models.BooleanField()
#     checkOut = models.BooleanField()

#     def __str__(self):
#         return self.userid

#     class Meta:
#         managed = True
#         db_table = 'lodge'

class Owner_Utility(models.Model):
    number_var = models.IntegerField(blank=False,null=False)
    is_table = models.BooleanField(default=False)
    room_number = models.BooleanField(default=False)
    is_booked = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    image1 = CloudinaryField(blank=False)
    image2 = CloudinaryField(blank=False)
    image3 = CloudinaryField(blank=False)
    image4 = CloudinaryField(blank=False)
    description = models.CharField(blank=False,max_length=250)
    room_price = models.IntegerField(blank=False,null=False)
    class Meta:
        managed = True
        db_table = 'owner_utility'


