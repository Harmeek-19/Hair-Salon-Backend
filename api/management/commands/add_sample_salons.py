from django.core.management.base import BaseCommand
from api.models import Salon

class Command(BaseCommand):
    help = 'Adds sample salon data to the database'

    def handle(self, *args, **kwargs):
        salons_data = [
            {"name": "Glamour Cuts", "latitude": 40.7128, "longitude": -74.0060, "address": "123 Broadway, New York, NY"},
            {"name": "Chic Styles", "latitude": 40.7589, "longitude": -73.9851, "address": "456 5th Ave, New York, NY"},
            {"name": "Elegance Hair", "latitude": 40.7549, "longitude": -73.9840, "address": "789 Madison Ave, New York, NY"},
            {"name": "Beauty Lounge", "latitude": 34.0522, "longitude": -118.2437, "address": "321 Hollywood Blvd, Los Angeles, CA"},
            {"name": "Scissors & Combs", "latitude": 41.8781, "longitude": -87.6298, "address": "555 Michigan Ave, Chicago, IL"},
        ]

        for salon_data in salons_data:
            Salon.objects.create(**salon_data)
            self.stdout.write(self.style.SUCCESS(f'Successfully added salon "{salon_data["name"]}"'))