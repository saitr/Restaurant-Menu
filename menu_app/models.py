
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import qrcode
from django.core.files import File
from PIL import Image,ImageDraw
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from cloudinary.models import CloudinaryField
from .manager import CustomUserManager
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from urllib.parse import urlencode

from rest_framework.authtoken.models import Token
import secrets

class CustomUser(AbstractUser, PermissionsMixin):
    phone_number = models.CharField(max_length=20,unique=True,null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    is_chef = models.BooleanField(default=False)
    otp = models.CharField(max_length=20)
    username = models.CharField(max_length=150, unique=True, null=True)
    password = models.CharField(max_length=100,null=False,blank=False)
    email = models.EmailField(unique=True)
    address = models.TextField(max_length=250)
    jwt_token = models.CharField(max_length=250,unique=True,null=True)
    token = models.CharField(max_length=100,unique=True,null=True,blank=True)
    is_logged_in = models.BooleanField(default=False)
    display_picture = CloudinaryField('Display Picture',null=True, blank=True)
    objects = CustomUserManager()

    # Use 'phone_number' as the unique identifier for authentication
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username','email']

    class Meta:
        db_table = 'CustomUser'

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

    
class Categories(models.Model):
    categoryName = models.CharField(max_length=255)
    category_img = CloudinaryField(blank=True)

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

class Owner_Utility(models.Model):
    table_number = models.IntegerField(default=False)
    qr_code = models.ImageField(upload_to='qr_code',  blank=True)
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

#
# def generate_qr_code(sender, instance, **kwargs):
#     if not instance.qr_code:
#         # Assuming 'table_number' is already set on the instance
#         url = f'http://127.0.0.1:8000/category_api/{instance.table_number}'
#
#         qr_code_img = qrcode.make(url)
#         canvas = Image.new('RGB', (350, 350), 'white')
#         draw = ImageDraw.Draw(canvas)
#         canvas.paste(qr_code_img)
#
#         buffer = BytesIO()
#         canvas.save(buffer, format='PNG')
#
#         instance.qr_code.save(f'{instance.table_number}.png', File(buffer), save=False)
#
# models.signals.pre_save.connect(generate_qr_code, sender=Owner_Utility)

# import qrcode
# from io import BytesIO
# from django.core.files import File


def generate_qr_code(sender, instance, **kwargs):
    if not instance.qr_code:
        # Assuming 'table_number' is already set on the instance
        url = f'http://127.0.0.1:8000/category_api/{instance.table_number}'
        params = {'url': url}
        url_encoded = urlencode(params)
        qr_code_img = qrcode.make(f'URL:{url_encoded}')

        buffer = BytesIO()
        qr_code_img.save(buffer, format='PNG')

        instance.qr_code.save(f'{instance.table_number}.png', File(buffer), save=False)
        instance.save()

models.signals.pre_save.connect(generate_qr_code, sender=Owner_Utility)

class Order(models.Model):
    table_number = models.ForeignKey(Owner_Utility, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(null=False, blank=False)
    generate_bill = models.BooleanField(default=False)
    class Meta:
        managed = True
        db_table = 'order'


class SubOrder(models.Model):
    table_number = models.ForeignKey(Owner_Utility, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(null=False, blank=False)
    order_deliverd = models.BooleanField(default=False)
    order_place = models.BooleanField(default=False)
    main_orderid = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        managed = True
        db_table = 'suborder'



class Cart(models.Model):
    table_number = models.ForeignKey(Owner_Utility,on_delete=models.CASCADE)
    items = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=False, default=1)
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    cart_created = models.BooleanField(default=False)
    sub_order_id = models.ForeignKey(SubOrder, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        managed = True
        db_table = 'cart'



class Order_Items(models.Model):
    quantity = models.IntegerField()
    order_item_price = models.IntegerField()
    item_id = models.ForeignKey(Items, on_delete=models.CASCADE)
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    sub_order_id = models.ForeignKey(SubOrder, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'order_Items'



# Sai models 



