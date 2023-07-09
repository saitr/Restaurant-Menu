# Generated by Django 4.2.2 on 2023-07-04 10:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging_app', '0007_remove_lodge_id_alter_lodge_number_of_people'),
    ]

    operations = [
        migrations.AddField(
            model_name='lodge',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lodge',
            name='number_of_people',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')]),
        ),
    ]
