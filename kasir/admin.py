from django.contrib import admin
from .models import Customer, Transaksi, ItemTransaksi
from gudang.models import Produk

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('nama', 'alamat', 'no_telepon')
    search_fields = ('nama',)  # Menambahkan pencarian berdasarkan nama

class ItemTransaksiInline(admin.TabularInline):
    model = ItemTransaksi
    extra = 1  # Jumlah form kosong yang ditampilkan

class TransaksiAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'metode_pembayaran', 'tanggal')  # Hapus atribut yang tidak ada
    inlines = [ItemTransaksiInline]  # Menambahkan inline untuk item transaksi

admin.site.register(Transaksi, TransaksiAdmin)