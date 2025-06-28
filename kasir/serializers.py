from rest_framework import serializers
from .models import Customer, Closing
from gudang.models import Produk # Pastikan path import ini benar

class CustomerSerializer(serializers.ModelSerializer):
    """Serializer untuk Customer, ini sudah benar."""
    class Meta:
        model = Customer
        fields = ['id', 'nama', 'alamat', 'no_telepon']

class ClosingSerializer(serializers.ModelSerializer):
    """
    Serializer untuk Closing yang sudah diperbaiki.
    Sekarang menyertakan nama produk dan customer.
    """
    # Menambahkan field baru 'product_name'.
    # `source='produk.nama'` akan mengambil nama dari relasi ForeignKey 'produk'.
    # Asumsi: model Produk Anda memiliki field bernama 'nama'.
    product_name = serializers.CharField(source='produk.nama', read_only=True)

    # Menambahkan field baru 'customer_name'.
    # `source='customer.nama'` mengambil nama dari relasi 'customer'.
    # `allow_null=True` karena relasi customer bisa kosong (null=True di model).
    customer_name = serializers.CharField(source='customer.nama', read_only=True, allow_null=True)

    class Meta:
        model = Closing
        # Tentukan semua field yang ingin ditampilkan di API,
        # termasuk field baru yang kita buat.
        fields = [
            'id',
            'product_name',   # <-- Nama produk
            'customer_name',  # <-- Nama customer
            'qty',
            'payment_method',
            'total_transaksi',
            'tanggal',
            'produk',         # <-- ID produk (opsional, bisa disimpan)
            'customer'        # <-- ID customer (opsional, bisa disimpan)
        ]