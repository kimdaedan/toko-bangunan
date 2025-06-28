from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Tambahkan ClosingDetailAPIView ke import
from .views import ClosingAPIView, CustomerViewSet, ExpenseViewSet, ClosingDetailAPIView

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    # URL untuk daftar dan membuat transaksi baru
    path('kasir/closing/', ClosingAPIView.as_view(), name='api-closing-list'),

    # URL BARU: Untuk detail, update, dan delete satu transaksi
    path('kasir/closing/<int:pk>/', ClosingDetailAPIView.as_view(), name='api-closing-detail'),

    path('', include(router.urls)),
]
