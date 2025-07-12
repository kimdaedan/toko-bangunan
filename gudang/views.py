from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

# Impor model dan serializer dari aplikasi 'gudang'
from .models import Produk, Pengeluaran
from .serializers import ProdukSerializer, PengeluaranSerializer
from .pagination import CustomPaginationWithTotal
# Impor kelas paginasi kustom.
from .pagination import CustomPaginationWithTotal

class ProdukViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk mengelola data Produk.
    """
    queryset = Produk.objects.all().order_by('nama')
    serializer_class = ProdukSerializer

     # --- PERBAIKAN: Menambahkan fungsionalitas pencarian ---
    filter_backends = [filters.SearchFilter]
    # Tentukan field mana saja yang bisa dicari.
    # Anda bisa menambahkan field lain jika perlu, misal: 'deskripsi'
    search_fields = ['nama']

    @action(detail=True, methods=['post'])
    def add_stock(self, request, pk=None):
        """
        Action kustom untuk menambah stok pada produk tertentu.
        URL: /api/gudang/produk/{id}/add_stock/
        """
        try:
            # Dapatkan objek produk yang akan diupdate
            product = self.get_object()

            # Ambil jumlah stok yang akan ditambahkan dari data request
            quantity_to_add = request.data.get('quantity')

            # Validasi input
            if quantity_to_add is None:
                return Response({'error': 'Jumlah (quantity) diperlukan.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                quantity_to_add = int(quantity_to_add)
                if quantity_to_add <= 0:
                    raise ValueError()
            except (ValueError, TypeError):
                return Response({'error': 'Jumlah (quantity) harus berupa angka positif.'}, status=status.HTTP_400_BAD_REQUEST)

            # Tambah stok dan simpan
            product.jumlah += quantity_to_add
            product.save()

            # Kembalikan data produk yang sudah diupdate
            serializer = self.get_serializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class PengeluaranViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk Pengeluaran dengan filter tanggal canggih.
    """
    queryset = Pengeluaran.objects.all().order_by('-date')
    serializer_class = PengeluaranSerializer
    pagination_class = CustomPaginationWithTotal

    def update(self, request, *args, **kwargs):
        """
        Kustomisasi metode update agar hanya bisa mengubah payment_status.
        """
        instance = self.get_object()

        # Hanya proses field 'payment_status' dari data yang dikirim
        new_status = request.data.get('payment_status')

        # Validasi sederhana
        if new_status not in ['paid', 'unpaid']:
            return Response(
                {'error': "Nilai status tidak valid. Gunakan 'paid' atau 'unpaid'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update instance dan simpan
        instance.payment_status = new_status
        instance.save()

        # Kembalikan data yang sudah diupdate
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # --- Logika Filter Baru ---
        period = request.query_params.get('period', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        today = timezone.now().date()

        if period == 'today':
            queryset = queryset.filter(date__date=today)
        elif period == 'yesterday':
            yesterday = today - timedelta(days=1)
            queryset = queryset.filter(date__date=yesterday)
        elif period == 'this_month':
            queryset = queryset.filter(date__year=today.year, date__month=today.month)
        elif period == 'last_month':
            first_day_of_current_month = today.replace(day=1)
            last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
            first_day_of_last_month = last_day_of_last_month.replace(day=1)
            queryset = queryset.filter(date__date__range=(first_day_of_last_month, last_day_of_last_month))
        elif period == 'this_year':
            queryset = queryset.filter(date__year=today.year)
        elif period == 'last_year':
            last_year = today.year - 1
            queryset = queryset.filter(date__year=last_year)
        else:
            # Gunakan custom date range jika 'period' tidak dipilih
            if start_date:
                queryset = queryset.filter(date__date__gte=start_date)
            if end_date:
                queryset = queryset.filter(date__date__lte=end_date)
        # --- Filter Selesai ---

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            self.paginator.page.paginator.object_list = queryset
            return self.paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)