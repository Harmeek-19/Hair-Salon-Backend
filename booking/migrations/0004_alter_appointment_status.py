# Generated by Django 5.0.7 on 2024-08-03 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_alter_appointment_services'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('booked', 'Booked'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], max_length=20),
        ),
    ]
