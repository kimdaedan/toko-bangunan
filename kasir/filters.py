    import django_filters
    from .models import Closing

    class ClosingFilter(django_filters.FilterSet):
        # Filter berdasarkan nama customer (icontains = case-insensitive contains)
        customer_name = django_filters.CharFilter(field_name='customer__nama', lookup_expr='icontains')

        # Filter berdasarkan tanggal mulai (gte = greater than or equal to)
        start_date = django_filters.DateFilter(field_name='tanggal__date', lookup_expr='gte')

        # Filter berdasarkan tanggal akhir (lte = less than or equal to)
        end_date = django_filters.DateFilter(field_name='tanggal__date', lookup_expr='lte')

        class Meta:
            model = Closing
            # Definisikan field yang bisa digunakan untuk filter
            fields = ['customer_name', 'start_date', 'end_date']
