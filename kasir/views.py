from rest_framework import viewsets
from .models import Customer, Transaksi
from .serializers import CustomerSerializer, TransaksiSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()  # Pastikan ini ada
    serializer_class = CustomerSerializer

class TransaksiViewSet(viewsets.ViewSet):
    # Jika TransaksiViewSet tidak menggunakan ModelViewSet, pastikan untuk mendefinisikan basename
    def create(self, request):
        serializer = TransaksiSerializer(data=request.data)
        if serializer.is_valid():
            produk_id = serializer.validated_data['produk'].id
            jumlah = serializer.validated_data['jumlah']

            try:
                produk_obj = Produk.objects.get(id=produk_id)
            except Produk.DoesNotExist:
                return Response({'error': 'Produk tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)

            if produk_obj.stok >= jumlah:
                produk_obj.stok -= jumlah
                produk_obj.save()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response({'error': 'Stok tidak cukup'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)