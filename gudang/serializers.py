from rest_framework import serializers
from .models import Produk, Pengeluaran  # Pastikan kedua model diimpor

class ProdukSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produk
        fields = '__all__'  # Ini akan mencakup semua field, termasuk gambar

class PengeluaranSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pengeluaran
        fields = '__all__'  # Ini akan mencakup semua field, termasuk nama