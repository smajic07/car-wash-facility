# Generated by Django 3.2.5 on 2022-07-17 14:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_wash_facility', '0005_alter_customers_car_wash_programs_date_of_car_wash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='address',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='customers',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customers',
            name='email',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='customers_car_wash_programs',
            name='date_of_car_wash',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='customers_car_wash_programs',
            name='end_hours',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customers_car_wash_programs',
            name='end_minutes',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customers_car_wash_programs',
            name='start_hours',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customers_car_wash_programs',
            name='start_minutes',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]