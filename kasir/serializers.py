from rest_framework import serializers
from .models import Customer, Transaksi
from gudang.models import Produk

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'nama', 'alamat', 'no_telepon']  # Menampilkan field yang ada

class TransaksiSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    produk = serializers.PrimaryKeyRelatedField(queryset=Produk.objects.all())

    class Meta:
        model = Transaksi
        fields = ['customer', 'produk', 'metode_pembayaran', 'jumlah', 'tanggal']  # Tambahkan tanggal jika perlu

    def create(self, validated_data):
        # Logika untuk mengurangi stok produk ketika transaksi dibuat
        produk_id = validated_data['produk']
        jumlah = validated_data['jumlah']

        # Ambil objek produk dan cek stok
        produk = Produk.objects.get(id=produk_id)
        if produk.stok >= jumlah:
            produk.stok -= jumlah
            produk.save()  # Simpan perubahan stok
            return super().create(validated_data)
        else:
            raise serializers.ValidationError("Stok tidak cukup untuk produk ini.")