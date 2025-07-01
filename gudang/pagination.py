from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Sum

# Impor model yang relevan untuk menentukan field total
from .models import Pengeluaran
from kasir.models import Closing

class CustomPaginationWithTotal(PageNumberPagination):
    """
    Kelas paginasi kustom yang menambahkan 'grand_total' ke dalam respons.
    """
    page_size = 25  # Jumlah item per halaman
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        # Tentukan field mana yang akan dijumlahkan berdasarkan model dari queryset
        model = self.page.paginator.object_list.model

        total_field = 'total_transaksi'  # Default untuk model Closing
        if model == Pengeluaran:
            # Jika modelnya adalah Pengeluaran, gunakan field 'amount'
            # Pastikan nama field 'amount' ini sesuai dengan yang ada di model Pengeluaran Anda
            total_field = 'amount'

        # Hitung total keseluruhan dari semua data di queryset (yang sudah difilter)
        grand_total = self.page.paginator.object_list.aggregate(
            total=Sum(total_field)
        )['total'] or 0

        # Kembalikan respons terstruktur yang berisi data, link, dan total
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'grand_total': grand_total, # <-- Menambahkan total keseluruhan
            'results': data
        })
