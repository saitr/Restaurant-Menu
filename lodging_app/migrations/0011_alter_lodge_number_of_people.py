# Generated by Django 4.2.2 on 2023-07-04 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging_app', '0010_alter_lodge_number_of_people'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lodge',
            name='number_of_people',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=4),
        ),
    ]
