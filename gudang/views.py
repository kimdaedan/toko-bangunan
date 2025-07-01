from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Sum

# Impor model dan serializer dari aplikasi 'gudang'
from .models import Produk, Pengeluaran
from .serializers import ProdukSerializer, PengeluaranSerializer

# Impor kelas paginasi kustom dari file pagination.py di dalam aplikasi gudang
from .pagination import CustomPaginationWithTotal

class ProdukViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk mengelola data Produk.
    """
    queryset = Produk.objects.all().order_by('nama')
    serializer_class = ProdukSerializer

class PengeluaranViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk mengelola data Pengeluaran dengan filter dan total.
    """
    queryset = Pengeluaran.objects.all().order_by('-date')
    serializer_class = PengeluaranSerializer
    # Terapkan kelas paginasi kustom
    pagination_class = CustomPaginationWithTotal

    def list(self, request, *args, **kwargs):
        """
        Kustomisasi metode list untuk menambahkan filter tanggal dan grand_total.
        """
        # Mulai dengan queryset dasar
        queryset = self.get_queryset()

        # --- Logika Filter Manual ---
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        # --- Filter Selesai ---

        # Lakukan paginasi pada queryset yang SUDAH difilter
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # Beri tahu paginator queryset mana yang harus digunakan untuk menghitung total
            self.paginator.page.paginator.object_list = queryset
            return self.paginator.get_paginated_response(serializer.data)

        # Fallback jika tidak ada paginasi
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
