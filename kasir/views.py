from rest_framework import viewsets, status, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q # <-- Impor Q untuk query kompleks
from django.db import transaction

# Impor kelas paginasi
from .pagination import CustomPaginationWithTotal

# Impor semua model dan serializer yang dibutuhkan
from .models import Closing, Customer, Expense
from gudang.models import Produk as GudangProduk
from .serializers import ClosingSerializer, CustomerSerializer, ExpenseSerializer

class ClosingAPIView(APIView):
    pagination_class = CustomPaginationWithTotal

    def get(self, request, *args, **kwargs):
        """Menangani GET request dengan filter manual dan paginasi."""
        queryset = Closing.objects.select_related('produk', 'customer').all().order_by('-tanggal')

        # --- FILTER MANUAL DIMULAI DI SINI ---

        # Ambil parameter dari URL
        search_query = request.query_params.get('customer_name', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        # Terapkan filter jika parameter ada
        if search_query:
            # Filter berdasarkan nama customer (case-insensitive)
            queryset = queryset.filter(customer__nama__icontains=search_query)

        if start_date:
            # Filter tanggal lebih besar atau sama dengan start_date
            queryset = queryset.filter(tanggal__date__gte=start_date)

        if end_date:
            # Filter tanggal lebih kecil atau sama dengan end_date
            queryset = queryset.filter(tanggal__date__lte=end_date)

        # --- FILTER MANUAL SELESAI ---

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)

        if page is not None:
            serializer = ClosingSerializer(page, many=True)
            # Beri tahu paginator untuk menghitung total dari queryset yang sudah difilter
            paginator.page.paginator.object_list = queryset
            return paginator.get_paginated_response(serializer.data)

        serializer = ClosingSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # Metode POST Anda tidak perlu diubah
        # ... (kode lengkap dari respons sebelumnya)
        pass

# ... (ClosingDetailAPIView, CustomerViewSet, dan ExpenseViewSet tetap sama) ...
class ClosingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Closing.objects.all()
    serializer_class = ClosingSerializer
    # ...

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('nama')
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nama', 'alamat', 'no_telepon']

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-date')
    serializer_class = ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk mengelola data pengeluaran dengan filter dan total.
    """
    queryset = Expense.objects.all().order_by('-date')
    serializer_class = ExpenseSerializer
    # Kita akan menggunakan paginasi yang sama seperti di Closing
    pagination_class = CustomPaginationWithTotal

    def list(self, request, *args, **kwargs):
        """
        Kustomisasi metode list untuk menambahkan filter tanggal dan grand_total.
        """
        # Mulai dengan queryset dasar
        queryset = self.get_queryset()

        # --- Filter Manual ---
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
            # Dapatkan respons paginasi (yang sudah berisi grand_total dari kelas pagination)
            # Kita perlu memberitahu paginator queryset mana yang harus digunakan untuk menghitung total
            self.paginator.page.paginator.object_list = queryset
            return self.paginator.get_paginated_response(serializer.data)

        # Fallback jika tidak ada paginasi
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)