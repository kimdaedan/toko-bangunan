from rest_framework import serializers
from .models import Produk, Pengeluaran  # Pastikan kedua model diimpor

class ProdukSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produk
        fields = '__all__'  # Ini akan mencakup semua field, termasuk gambar

class PengeluaranSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField()
    class Meta:
        model = Pengeluaran
        fields = ['date', 'category', 'amount', 'payment_status']

    def validate_date(self, value):
        return value.date()