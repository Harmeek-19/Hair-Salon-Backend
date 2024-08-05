from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Salon, Stylist, Service
from .serializers import SalonSerializer, StylistSerializer, ServiceSerializer

class GlobalSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Please provide a search query.'}, status=status.HTTP_400_BAD_REQUEST)

        salons = Salon.objects.filter(
            Q(name__icontains=query) | 
            Q(address__icontains=query) | 
            Q(description__icontains=query)
        )
        stylists = Stylist.objects.filter(
            Q(name__icontains=query) | 
            Q(specialties__icontains=query)
        )
        services = Service.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )

        results = {
            'salons': SalonSerializer(salons, many=True).data,
            'stylists': StylistSerializer(stylists, many=True).data,
            'services': ServiceSerializer(services, many=True).data,
        }

        return Response(results)