from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, viewsets, filters
from django.db import transaction

# Import semua model dan serializer yang dibutuhkan
from .models import Closing, Customer, Expense
from gudang.models import Produk as GudangProduk
from .serializers import ClosingSerializer, CustomerSerializer, ExpenseSerializer
from .pagination import CustomPaginationWithTotal


class ClosingAPIView(APIView):
    pagination_class = CustomPaginationWithTotal

    def get(self, request, *args, **kwargs):
        """Menangani GET request dengan filter manual dan paginasi."""
        # Mulai dengan mengambil semua data transaksi
        queryset = Closing.objects.select_related('produk', 'customer').all().order_by('-tanggal')

        # --- Logika Filter Manual ---

        # Ambil parameter dari URL, contoh: ?customer_name=juna&start_date=...
        search_query = request.query_params.get('customer_name', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        # Terapkan filter jika parameter ada isinya
        if search_query:
            # Filter berdasarkan nama customer (case-insensitive)
            # __nama adalah field di model Customer, __icontains adalah perintah 'contains'
            queryset = queryset.filter(customer__nama__icontains=search_query)

        if start_date:
            # Filter tanggal lebih besar atau sama dengan start_date
            queryset = queryset.filter(tanggal__date__gte=start_date)

        if end_date:
            # Filter tanggal lebih kecil atau sama dengan end_date
            queryset = queryset.filter(tanggal__date__lte=end_date)

        # --- Filter Selesai ---
# ini yang terbaru
        # Lakukan paginasi pada queryset yang SUDAH difilter
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)

        if page is not None:
            serializer = ClosingSerializer(page, many=True)
            # Beri tahu paginator untuk menghitung total dari queryset yang sudah difilter
            paginator.page.paginator.object_list = queryset
            return paginator.get_paginated_response(serializer.data)

        # Fallback jika tidak ada paginasi
        serializer = ClosingSerializer(queryset, many=True)
        return Response(serializer.data)
    def post(self, request, *args, **kwargs):
        """Menangani POST request untuk membuat transaksi closing baru."""
        data = request.data

        customer_id = data.get('customer')
        products_data = data.get('products')
        payment_method = data.get('payment_method')

        if not products_data or not isinstance(products_data, list):
            return Response({'error': 'Format data produk tidak valid.'}, status=status.HTTP_400_BAD_REQUEST)

        customer = None
        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                return Response({'error': f'Customer dengan ID {customer_id} tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                created_transactions = []
                for product_data in products_data:
                    product_id = product_data.get('id')
                    quantity = product_data.get('quantity')

                    if not all([product_id, quantity]):
                        raise ValueError("Data produk tidak lengkap.")

                    product_obj = GudangProduk.objects.select_for_update().get(id=product_id)

                    if product_obj.jumlah < quantity:
                        raise ValueError(f'Stok untuk "{product_obj.nama}" tidak mencukupi.')

                    product_obj.jumlah -= quantity
                    product_obj.save()

                    closing_entry = Closing.objects.create(
                        produk=product_obj,
                        customer=customer,
                        qty=quantity,
                        payment_method=payment_method,
                        total_transaksi=product_obj.harga * quantity
                    )
                    created_transactions.append(closing_entry.id)

            # Jika semua berhasil, kembalikan respons sukses
            return Response(
                {'message': 'Transaksi berhasil dibuat.', 'transaction_ids': created_transactions},
                status=status.HTTP_201_CREATED
            )

        except GudangProduk.DoesNotExist:
            return Response({'error': 'Salah satu produk tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Terjadi kesalahan internal pada server.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ... (Kelas View lainnya tetap sama) ...
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
    pagination_class = CustomPaginationWithTotal
    # ...
