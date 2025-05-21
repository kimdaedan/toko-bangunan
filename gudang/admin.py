from django.contrib import admin
from .models import Produk, Pengeluaran, Kategori

@admin.register(Produk)
class ProdukAdmin(admin.ModelAdmin):
    list_display = ('nama', 'jumlah', 'harga', 'gambar')

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('nama',)

@admin.register(Pengeluaran)
class PengeluaranAdmin(admin.ModelAdmin):
    list_display = ('nama', 'tanggal', 'kategori', 'jumlah')