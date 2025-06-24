from rest_framework import serializers
from .models import Customer, Transaksi, ItemTransaksi  # Pastikan ItemTransaksi ada
from gudang.models import Produk

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'nama', 'alamat', 'no_telepon']

class ItemTransaksiSerializer(serializers.ModelSerializer):
    produk_nama = serializers.CharField(source='produk.nama', read_only=True)

    class Meta:
        model = ItemTransaksi
        fields = ['id', 'produk', 'produk_nama', 'jumlah', 'harga_satuan', 'subtotal']
        extra_kwargs = {
            'harga_satuan': {'read_only': True},
            'subtotal': {'read_only': True}
        }

class TransaksiSerializer(serializers.ModelSerializer):
    items = ItemTransaksiSerializer(many=True)
    customer_detail = CustomerSerializer(source='customer', read_only=True)
    total_harga = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Transaksi
        fields = ['id', 'customer', 'customer_detail', 'metode_pembayaran',
                  'tanggal', 'items', 'total_harga']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        transaksi = Transaksi.objects.create(**validated_data)

        for item_data in items_data:
            produk = item_data['produk']
            jumlah = item_data['jumlah']

            if produk.stok < jumlah:
                transaksi.delete()
                raise serializers.ValidationError(
                    {'error': f'Stok {produk.nama} tidak cukup. Stok tersedia: {produk.stok}'}
                )

            # Kurangi stok produk
            produk.stok -= jumlah
            produk.save()

            # Buat item transaksi
            ItemTransaksi.objects.create(
                transaksi=transaksi,
                produk=produk,
                jumlah=jumlah,
                harga_satuan=produk.harga,  # Pastikan harga satuan diambil dari produk
                subtotal=produk.harga * jumlah  # Hitung subtotal
            )

        return transaksi