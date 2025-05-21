from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdukViewSet, PengeluaranViewSet

router = DefaultRouter()
router.register(r'produk', ProdukViewSet)
router.register(r'pengeluaran', PengeluaranViewSet)

urlpatterns = [
    path('', include(router.urls)),
]