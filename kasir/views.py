from rest_framework import generics, viewsets # <-- PASTIKAN 'viewsets' ADA DI SINI
from .models import Closing, Customer
from .serializers import ClosingSerializer, CustomerSerializer

# View ini untuk menampilkan daftar closing
class ClosingListView(generics.ListAPIView):
    serializer_class = ClosingSerializer

    def get_queryset(self):
        return Closing.objects.select_related('produk', 'customer').all().order_by('-tanggal')

# ViewSet ini untuk mengelola data customer (CRUD)
class CustomerViewSet(viewsets.ModelViewSet): #<-- Baris ini butuh 'viewsets' dari import
    """
    API endpoint yang memungkinkan customer untuk dilihat atau diubah (CRUD).
    """
    queryset = Customer.objects.all().order_by('nama')
    serializer_class = CustomerSerializer