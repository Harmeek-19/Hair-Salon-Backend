# Generated by Django 5.0.7 on 2024-08-03 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_alter_appointment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('BOOKED', 'Booked'), ('CONFIRMED', 'Confirmed'), ('CANCELLED', 'Cancelled')], default='BOOKED', max_length=20),
        ),
    ]
