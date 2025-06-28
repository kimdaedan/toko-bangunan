from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Sum

class CustomPaginationWithTotal(PageNumberPagination):
    page_size = 25  # Jumlah item per halaman
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        # Hitung total keseluruhan dari semua transaksi di queryset
        grand_total = self.page.paginator.object_list.aggregate(
            total=Sum('total_transaksi')
        )['total'] or 0

        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'grand_total': grand_total, # <-- Menambahkan total keseluruhan
            'results': data
        })
