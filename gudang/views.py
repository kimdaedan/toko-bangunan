from rest_framework import viewsets
from .models import Produk, Pengeluaran  # Impor model
from .serializers import ProdukSerializer, PengeluaranSerializer  # Impor serializer

class ProdukViewSet(viewsets.ModelViewSet):
    queryset = Produk.objects.all()
    serializer_class = ProdukSerializer

class PengeluaranViewSet(viewsets.ModelViewSet):
    queryset = Pengeluaran.objects.all()
    serializer_class = PengeluaranSerializer

