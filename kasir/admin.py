from django.contrib import admin
from .models import Customer, Closing

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('nama', 'alamat', 'no_telepon')
    search_fields = ('nama',)

class ClosingAdmin(admin.ModelAdmin):
    list_display = ('id', 'produk', 'customer', 'qty', 'payment_method', 'total_transaksi', 'tanggal')  # Menambahkan 'tanggal'
    list_filter = ('payment_method', 'tanggal')  # Menambahkan filter berdasarkan metode pembayaran dan tanggal
    search_fields = ('customer__nama', 'produk__nama')  # Memungkinkan pencarian berdasarkan nama customer dan produk

admin.site.register(Closing, ClosingAdmin)