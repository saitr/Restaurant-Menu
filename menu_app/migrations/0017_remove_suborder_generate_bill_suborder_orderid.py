# Generated by Django 4.2.2 on 2023-07-13 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu_app', '0016_remove_order_order_deliverd_remove_order_order_place_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suborder',
            name='generate_bill',
        ),
        migrations.AddField(
            model_name='suborder',
            name='orderid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='menu_app.order'),
        ),
    ]
