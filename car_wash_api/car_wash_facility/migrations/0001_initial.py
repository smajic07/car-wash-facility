# Generated by Django 3.2.5 on 2022-07-14 14:31

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car_Wash_Programs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('steps', models.CharField(max_length=1000)),
                ('duration_in_minutes', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('postal_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('address', models.CharField(max_length=200)),
                ('number_of_car_washes', models.IntegerField(default=0)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('id_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_wash_facility.cities')),
            ],
        ),
        migrations.CreateModel(
            name='Customers_Car_Wash_Programs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_car_wash', models.DateField(default=datetime.date.today)),
                ('start_hours', models.IntegerField()),
                ('start_minutes', models.IntegerField()),
                ('end_hours', models.IntegerField()),
                ('end_minutes', models.IntegerField()),
                ('id_car_wash_program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_wash_facility.car_wash_programs')),
                ('id_customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_wash_facility.customers')),
            ],
        ),
    ]