# Generated by Django 3.2.5 on 2022-07-16 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_wash_facility', '0004_customers_car_wash_programs_with_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers_car_wash_programs',
            name='date_of_car_wash',
            field=models.DateField(),
        ),
    ]