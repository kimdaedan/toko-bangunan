from rest_framework import viewsets, status, generics, filters  # <-- PERBAIKAN: Import filters di sini
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction

# Impor kelas paginasi yang baru dibuat
from .pagination import CustomPaginationWithTotal

# Import semua model dan serializer yang dibutuhkan
from .models import Closing, Customer, Expense
from gudang.models import Produk as GudangProduk
from .serializers import ClosingSerializer, CustomerSerializer, ExpenseSerializer

class ClosingAPIView(APIView):
    """
    API View untuk menghandle transaksi closing.
    """
    pagination_class = CustomPaginationWithTotal

    def get(self, request, *args, **kwargs):
        """Menangani GET request dengan paginasi."""
        queryset = Closing.objects.select_related('produk', 'customer').all().order_by('-tanggal')

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)

        if page is not None:
            serializer = ClosingSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = ClosingSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # Metode POST Anda yang sudah ada
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

class ClosingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Closing.objects.all()
    serializer_class = ClosingSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        payment_method = request.data.get('payment_method')
        if payment_method is None:
            return Response({'error': 'Field payment_method diperlukan.'}, status=status.HTTP_400_BAD_REQUEST)
        instance.payment_method = payment_method
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('nama')
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nama', 'alamat', 'no_telepon']

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-date')
    serializer_class = ExpenseSerializer
