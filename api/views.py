from django.db.models import Count, Sum
from rest_framework import viewsets, serializers, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action, api_view, permission_classes
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import Salon, Stylist, Service, Promotion
from booking.models import Appointment
from content.models import Review, Blog
from .serializers import (SalonSerializer, StylistSerializer, ServiceSerializer, AppointmentSerializer, ReviewSerializer, BlogSerializer, PromotionSerializer)
from authentication.models import User
from .permissions import IsSalonOwnerOrReadOnly, IsAdminUserOrReadOnly, IsStylist, IsSalonOwner
from .reports import get_salon_report, get_stylist_report, get_appointment_report

class TestAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Authentication successful!"})

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'price', 'salon']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'duration']

class SalonViewSet(viewsets.ModelViewSet):
    queryset = Salon.objects.all()
    serializer_class = SalonSerializer
    permission_classes = [IsAuthenticated, IsSalonOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'address', 'city', 'country_code', 'services__price']
    search_fields = ['name', 'address', 'email', 'description']
    ordering_fields = ['name', 'id', 'rating']

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        lat = float(request.query_params.get('lat', 0))
        lon = float(request.query_params.get('lon', 0))
        user_location = Point(lon, lat, srid=4326)
        
        nearby_salons = Salon.objects.annotate(
            distance=Distance('location', user_location)
        ).order_by('distance')[:6]
        
        serializer = self.get_serializer(nearby_salons, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stylists(self, request, pk=None):
        salon = self.get_object()
        stylists = salon.stylists.all()
        serializer = StylistSerializer(stylists, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        salon = self.get_object()
        appointments = Appointment.objects.filter(stylist__salon=salon)
        popular_services = Service.objects.filter(appointment__in=appointments).annotate(count=Count('appointment')).order_by('-count')[:5]
        revenue = appointments.filter(status='COMPLETED').aggregate(total=Sum('service__price'))['total'] or 0
        
        data = {
            'total_appointments': appointments.count(),
            'completed_appointments': appointments.filter(status='COMPLETED').count(),
            'popular_services': [{'name': s.name, 'count': s.count} for s in popular_services],
            'total_revenue': revenue,
        }
        return Response(data)

    @action(detail=True, methods=['post'])
    def claim(self, request, pk=None):
        salon = self.get_object()
        if salon.owner:
            return Response({"detail": "This salon is already claimed."}, status=status.HTTP_400_BAD_REQUEST)
        
        salon.owner = request.user
        salon.save()
        return Response({"detail": "Salon claim request submitted for review."})

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        top_salons = self.get_queryset().order_by('-rating')[:4]
        serializer = self.get_serializer(top_salons, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recommended(self, request):
        return self.top_rated(request)

class StylistViewSet(viewsets.ModelViewSet):
    queryset = Stylist.objects.all()
    serializer_class = StylistSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'specialties', 'salon', 'workplace']
    search_fields = ['name', 'specialties', 'email']
    ordering_fields = ['name', 'years_of_experience']

    @action(detail=True, methods=['get'])
    def appointments(self, request, pk=None):
        stylist = self.get_object()
        appointments = Appointment.objects.filter(stylist=stylist)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def available_slots(self, request, pk=None):
        stylist = self.get_object()
        date = request.query_params.get('date', datetime.now().date())
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d').date()
        
        start_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=9)
        end_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=17)
        
        booked_slots = Appointment.objects.filter(stylist=stylist, date=date).values_list('time', flat=True)
        
        available_slots = []
        current_slot = start_time
        while current_slot < end_time:
            if current_slot.time() not in booked_slots:
                available_slots.append(current_slot.strftime('%H:%M'))
            current_slot += timedelta(minutes=30)
        
        return Response(available_slots)

    @action(detail=True, methods=['post'])
    def claim(self, request, pk=None):
        stylist = self.get_object()
        if stylist.user:
            return Response({"detail": "This stylist profile is already claimed."}, status=status.HTTP_400_BAD_REQUEST)
        
        stylist.user = request.user
        stylist.save()
        return Response({"detail": "Stylist profile claim request submitted for review."})

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['stylist', 'service', 'date', 'status']
    search_fields = ['client_name', 'client_email']
    ordering_fields = ['date', 'time']

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'CONFIRMED'
        appointment.save()
        return Response({'status': 'appointment confirmed'})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'CANCELLED'
        appointment.save()
        return Response({'status': 'appointment cancelled'})

    def perform_create(self, serializer):
        stylist = serializer.validated_data['stylist']
        date = serializer.validated_data['date']
        time = serializer.validated_data['time']
        
        if Appointment.objects.filter(stylist=stylist, date=date, time=time).exists():
            raise serializers.ValidationError("This time slot is already booked.")
        
        appointment = serializer.save()
        
        subject = 'New Appointment Booked'
        message = f'You have a new appointment on {appointment.date} at {appointment.time}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [appointment.stylist.email, appointment.client_email]
        send_mail(subject, message, from_email, recipient_list)

class ReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]

    @action(detail=False, methods=['get'])
    def salon_report(self, request):
        return Response(get_salon_report())

    @action(detail=False, methods=['get'])
    def stylist_report(self, request):
        return Response(get_stylist_report())

    @action(detail=False, methods=['get'])
    def appointment_report(self, request):
        return Response(get_appointment_report())

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def delete_review(self, request, pk=None):
        if request.user.is_staff or request.user.is_superuser:
            review = self.get_object()
            review.delete()
            return Response({"detail": "Review deleted successfully."})
        return Response({"detail": "You don't have permission to delete this review."}, status=status.HTTP_403_FORBIDDEN)

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]

class SuperAdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_users = User.objects.count()
        total_salons = Salon.objects.count()
        total_appointments = Appointment.objects.count()
        
        return Response({
            "total_users": total_users,
            "total_salons": total_salons,
            "total_appointments": total_appointments,
        })

class NotificationView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        message = request.data.get('message')
        users = User.objects.all()
        
        for user in users:
            # Implement your preferred method to send notifications here
            pass
        
        return Response({"detail": "Notifications sent successfully."})

class PromotionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_salon_with_stylists(request):
    salon_data = request.data.get('salon')
    stylists_data = request.data.get('stylists', [])

    # Create salon
    salon_serializer = SalonSerializer(data=salon_data)
    if salon_serializer.is_valid():
        salon = salon_serializer.save(owner=request.user)
        
        # Create stylists
        created_stylists = []
        for stylist_data in stylists_data:
            stylist_data['salon'] = salon.id
            stylist_serializer = StylistSerializer(data=stylist_data)
            if stylist_serializer.is_valid():
                stylist = stylist_serializer.save()
                created_stylists.append(stylist_serializer.data)
            else:
                return Response(stylist_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'salon': salon_serializer.data,
            'stylists': created_stylists
        }, status=status.HTTP_201_CREATED)
    
    return Response(salon_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsSalonOwner])
def delete_salon(request, salon_id):
    try:
        salon = Salon.objects.get(id=salon_id)
        salon.delete()
        return Response({"message": "Salon and associated stylists deleted successfully"}, status=status.HTTP_200_OK)
    except Salon.DoesNotExist:
        return Response({"error": "Salon not found"}, status=status.HTTP_404_NOT_FOUND)
