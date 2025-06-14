from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, TransaksiViewSet

router = DefaultRouter()
router.register(r'customer', CustomerViewSet)  # ModelViewSet dengan queryset
router.register(r'transaksi', TransaksiViewSet, basename='transaksi')  # Menambahkan basename

urlpatterns = [
    path('', include(router.urls)),
]