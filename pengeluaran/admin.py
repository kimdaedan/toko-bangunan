from django.contrib import admin
from .models import Pengeluaran, Kategori

class KategoriAdmin(admin.ModelAdmin):
    list_display = ('nama',)

admin.site.register(Kategori, KategoriAdmin)

class PengeluaranAdmin(admin.ModelAdmin):
    list_display = ('tanggal', 'nama_pengeluaran', 'kategori', 'jumlah')
    search_fields = ('nama_pengeluaran', 'kategori__nama')

admin.site.register(Pengeluaran, PengeluaranAdmin)