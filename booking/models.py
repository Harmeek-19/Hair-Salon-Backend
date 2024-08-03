# booking/models.py
from django.db import models
from authentication.models import User
from api.models import Salon, Stylist

class Appointment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    stylist = models.ForeignKey(Stylist, on_delete=models.CASCADE, related_name='appointments')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='appointments')
    service = models.TextField()  # Assuming you store service details as a text field
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=[('booked', 'Booked'), ('completed', 'Completed'), ('cancelled', 'Cancelled')])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
