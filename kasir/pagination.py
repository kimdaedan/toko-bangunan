from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Sum
from .models import Closing, Expense # Impor model

class CustomPaginationWithTotal(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        # Tentukan kolom mana yang akan dijumlahkan berdasarkan model
        model = self.page.paginator.object_list.model
        total_field = 'total_transaksi'
        if model == Expense:
            total_field = 'amount'

        # Hitung total keseluruhan dari queryset yang sudah difilter
        grand_total = self.page.paginator.object_list.aggregate(
            total=Sum(total_field)
        )['total'] or 0

        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'grand_total': grand_total,
            'results': data
        })
