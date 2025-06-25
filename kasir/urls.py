from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, ClosingViewSet

router = DefaultRouter()
router.register(r'customer', CustomerViewSet)  # ModelViewSet dengan queryset
router.register(r'closing', ClosingViewSet)  # Mendaftarkan ClosingViewSet

urlpatterns = [
    path('', include(router.urls)),  # Menggunakan satu urlpatterns
]