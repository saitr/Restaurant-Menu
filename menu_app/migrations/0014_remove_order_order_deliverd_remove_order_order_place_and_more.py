# Generated by Django 4.2.2 on 2023-07-13 00:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu_app', '0013_order_generate_bill'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_deliverd',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_place',
        ),
        migrations.CreateModel(
            name='SubOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.IntegerField()),
                ('order_deliverd', models.BooleanField(default=False)),
                ('order_place', models.BooleanField(default=False)),
                ('generate_bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu_app.order')),
                ('table_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu_app.owner_utility')),
            ],
            options={
                'db_table': 'suborder',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='sub_orderid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='menu_app.suborder'),
        ),
        migrations.AddField(
            model_name='order_items',
            name='sub_orderid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='menu_app.suborder'),
        ),
    ]
