from rest_framework import serializers
from api.models import Salon, Stylist, Service, Promotion
from booking.models import Appointment
from content.models import Review, Blog
from notifications.models import Notification


class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = '__all__'

class StylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stylist
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['customer', 'stylist', 'salon', 'service', 'date', 'start_time', 'end_time', 'status', 'total_price', 'notes']
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
    
class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'