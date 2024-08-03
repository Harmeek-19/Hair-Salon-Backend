# api/migrations/0002_create_sample_data.py
from django.db import migrations
import datetime
from django.contrib.auth.hashers import make_password

def create_sample_data(apps, schema_editor):
    User = apps.get_model('authentication', 'User')
    Salon = apps.get_model('api', 'Salon')
    Stylist = apps.get_model('api', 'Stylist')
    Service = apps.get_model('api', 'Service')
    Appointment = apps.get_model('booking', 'Appointment')

    # Create sample users for each role
    users = {
        'customer': User.objects.create(
            username='customer', 
            email='customer@example.com', 
            password=make_password('password123'), 
            role='customer',
            is_active=True
        ),
        'salon_owner': User.objects.create(
            username='owner', 
            email='owner@example.com', 
            password=make_password('password123'), 
            role='salon_owner',
            is_active=True
        ),
        'stylist': User.objects.create(
            username='stylist', 
            email='stylist@example.com', 
            password=make_password('password123'), 
            role='stylist',
            is_active=True
        ),
        'admin': User.objects.create(
            username='admin', 
            email='admin@example.com', 
            password=make_password('password123'), 
            role='admin',
            is_staff=True,
            is_active=True
        ),
        'super_admin': User.objects.create(
            username='superadmin', 
            email='superadmin@example.com', 
            password=make_password('password123'), 
            role='super_admin',
            is_staff=True,
            is_superuser=True,
            is_active=True
        ),
    }

    # Create sample salons
    salon1 = Salon.objects.create(
        name="Glamour Salon", 
        owner=users['salon_owner'], 
        address="123 Main St", 
        city="Metropolis", 
        phone="555-1234", 
        email="glamour@example.com"
    )
    salon2 = Salon.objects.create(
        name="Chic Cuts", 
        owner=users['salon_owner'], 
        address="456 Elm St", 
        city="Gotham", 
        phone="555-5678", 
        email="chic@example.com"
    )

    # Create sample stylists
    stylist1 = Stylist.objects.create(
        name="John Doe", 
        salon=salon1, 
        specialties="Haircut, Coloring", 
        years_of_experience=5,
        user=users['stylist']
    )
    stylist2 = Stylist.objects.create(
        name="Jane Smith", 
        salon=salon2, 
        specialties="Styling, Perms", 
        years_of_experience=8
    )

    # Create sample services
    service1 = Service.objects.create(name="Haircut", description="Basic haircut", price=30.00, duration=30)
    service2 = Service.objects.create(name="Coloring", description="Hair coloring", price=80.00, duration=120)

    # Create sample appointments
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    Appointment.objects.create(
        customer=users['customer'],
        stylist=stylist1,
        salon=salon1,
        service="Haircut",
        date=today,
        start_time=datetime.time(14, 0),
        end_time=datetime.time(15, 0),
        status="booked",
        total_price=30.00,
        notes="First appointment"
    )
    Appointment.objects.create(
        customer=users['customer'],
        stylist=stylist2,
        salon=salon2,
        service="Coloring",
        date=tomorrow,
        start_time=datetime.time(10, 0),
        end_time=datetime.time(12, 0),
        status="pending",
        total_price=80.00,
        notes="Client prefers organic products"
    )

class Migration(migrations.Migration):
    dependencies = [
        ('api', '0001_initial'),
        ('authentication', '0001_initial'),
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_data),
    ]