from django.db.models import Count, Avg
from .models import Salon, Stylist
from booking.models import Appointment

def get_salon_report():
    return Salon.objects.annotate(
        stylist_count=Count('stylists'),
        avg_rating=Avg('rating')
    ).values('id', 'name', 'stylist_count', 'avg_rating')

def get_stylist_report():
    return Stylist.objects.annotate(
        appointment_count=Count('appointment')
    ).values('id', 'name', 'appointment_count', 'years_of_experience')

def get_appointment_report():
    return Appointment.objects.values('status').annotate(count=Count('id'))