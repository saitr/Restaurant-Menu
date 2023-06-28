from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
# from jsonfield import JSONField
from  cloudinary.models import CloudinaryField
import uuid
# from .manager import CustomUserManager


class User(models.Model):
     username = models.CharField(max_length=255)
     phone_number = models.IntegerField()
     email_id = models.EmailField()
     is_verified = models.BooleanField()
     is_chef = models.BooleanField()
     password = models.CharField(max_length=255)

     def __str__(self):
         return self.phone_number

     class Meta:
         managed = True
         db_table = 'user'


class Categories(models.Model):
    categoryName = models.CharField(max_length=255)

    def __str__(self):
        return self.categoryName

    class Meta:
        managed = True
        db_table = 'categories'

class Items(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    itemName = models.CharField(max_length=255)
    itemPrice = models.IntegerField()
    item_image = CloudinaryField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.itemName

    class Meta:
        managed = True
        db_table = 'items'


class Cart(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.userId

    class Meta:
        managed = True
        db_table = 'cart'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField()

    def __str__(self):
        return self.table_number

    class Meta:
        managed = True
        db_table = 'order'

class Order_Items(models.Model):
    quantity = models.IntegerField()
    order_item_price = models.IntegerField()
    item_id = models.ForeignKey(Items, on_delete=models.CASCADE)
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_id

    class Meta:
        managed = True
        db_table = 'order_Items'

class Lodge(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    room_number = models.IntegerField()
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    identity_proof = CloudinaryField(blank=False)
    is_booked = models.BooleanField()
    checkIn = models.BooleanField()
    checkOut = models.BooleanField()

    def __str__(self):
        return self.userid

    class Meta:
        managed = True
        db_table = 'lodge'

class Owner_Utility(models.Model):
    number_var = models.IntegerField
    is_table = models.BooleanField(default=False)
    room_number = models.BooleanField(default=False)


    def __str__(self):
        return self.number_var

    class Meta:
        managed = True
        db_table = 'owner_utility'





