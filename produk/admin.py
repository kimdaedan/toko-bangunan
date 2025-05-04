from django.contrib import admin
from .models import Produk

@admin.register(Produk)
class ProdukAdmin(admin.ModelAdmin):
    list_display = ('nama', 'harga', 'stok')  # Kolom yang ditampilkan di admin
    search_fields = ('nama',)  # Fitur pencarian berdasarkan nama