from rest_framework import serializers
from .models import Closing, Customer, Expense # <-- Pastikan Expense sudah diimpor
from gudang.models import Produk

class ClosingSerializer(serializers.ModelSerializer):
    """Serializer untuk transaksi closing."""
    product_name = serializers.CharField(source='produk.nama', read_only=True)
    customer_name = serializers.CharField(source='customer.nama', read_only=True, allow_null=True)

    class Meta:
        model = Closing
        fields = [
            'id', 'product_name', 'customer_name', 'qty',
            'payment_method', 'total_transaksi', 'tanggal', 'produk', 'customer'
        ]

class CustomerSerializer(serializers.ModelSerializer):
    """Serializer untuk data customer."""
    class Meta:
        model = Customer
        fields = '__all__'

# --- TAMBAHKAN KELAS BARU DI BAWAH INI ---
class ExpenseSerializer(serializers.ModelSerializer):
    """Serializer untuk data pengeluaran."""
    class Meta:
        model = Expense
        fields = '__all__' # Ini akan menyertakan semua field dari model Expense, termasuk 'id'
