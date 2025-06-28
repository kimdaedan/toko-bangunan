from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClosingListView, CustomerViewSet

# 1. Router HANYA untuk mendaftarkan kelas ViewSet
router = DefaultRouter()
router.register(r'customers', CustomerViewSet)   # Daftarkan CustomerViewSet di sini

# 2. urlpatterns untuk semua URL Anda
urlpatterns = [
    # URL untuk ClosingListView (bukan ViewSet) menggunakan path() biasa
    path('kasir/closing/', ClosingListView.as_view(), name='api-closing-list'),

    # Sertakan URL dari router untuk CustomerViewSet
    path('', include(router.urls)),
]