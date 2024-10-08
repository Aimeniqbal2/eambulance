# Generated by Django 5.1.1 on 2024-09-21 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rapidapp', '0003_ambulance_driver_cnic_ambulance_driver_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergencyrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('dispatched', 'Dispatched'), ('on_route', 'On Route'), ('delivered', 'Delivered'), ('completed', 'Completed')], default='Pending', max_length=20),
        ),
    ]
