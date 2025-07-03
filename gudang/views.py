from rest_framework import viewsets
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

# Impor model, serializer, dan paginasi
from .models import Produk, Pengeluaran
from .serializers import ProdukSerializer, PengeluaranSerializer
from .pagination import CustomPaginationWithTotal
class ProdukViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk mengelola data Produk.
    """
    queryset = Produk.objects.all().order_by('nama')
    serializer_class = ProdukSerializer

class PengeluaranViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk Pengeluaran dengan filter tanggal canggih.
    """
    queryset = Pengeluaran.objects.all().order_by('-date')
    serializer_class = PengeluaranSerializer
    pagination_class = CustomPaginationWithTotal

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
