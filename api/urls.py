from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (SalonViewSet, StylistViewSet, ServiceViewSet, AppointmentViewSet,
                    TestAuthView, ReviewViewSet, BlogViewSet,
                    SuperAdminDashboardView, ReportViewSet, PromotionViewSet)
from . import views
router = DefaultRouter()
router.register(r'salons', SalonViewSet)
router.register(r'stylists', StylistViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'blogs', BlogViewSet)
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'promotions', PromotionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test-auth/', TestAuthView.as_view(), name='test-auth'),
    path('super-admin-dashboard/', SuperAdminDashboardView.as_view(), name='super-admin-dashboard'),
    path('coupons/', include('coupons.urls')),
    path('create-salon-with-stylists/', views.create_salon_with_stylists, name='create_salon_with_stylists'),
    path('delete-salon/<int:salon_id>/', views.delete_salon, name='delete_salon'),
]