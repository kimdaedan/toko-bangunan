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
    # Gunakan nama field yang sesuai dengan model
    list_display = ('name', 'date', 'category', 'amount')
    # Jika ingin menggunakan nama berbeda di admin:
    # list_display = ('get_nama', 'get_tanggal', 'get_kategori', 'get_jumlah')

    # Jika perlu custom display method
    def get_nama(self, obj):
        return obj.name
    get_nama.short_description = 'Nama'

    def get_tanggal(self, obj):
        return obj.date
    get_tanggal.short_description = 'Tanggal'

    def get_kategori(self, obj):
        return obj.category
    get_kategori.short_description = 'Kategori'

    def get_jumlah(self, obj):
        return f"Rp {obj.amount:,}"
    get_jumlah.short_description = 'Jumlah'