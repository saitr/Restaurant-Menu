# Generated by Django 4.2.2 on 2023-07-18 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
