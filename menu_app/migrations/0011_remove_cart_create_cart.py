# Generated by Django 4.2.2 on 2023-07-11 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu_app', '0010_cart_create_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='create_cart',
        ),
    ]
