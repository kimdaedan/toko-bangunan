from django.contrib import admin
from .models import Customer, Closing

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('nama', 'alamat', 'no_telepon')
    search_fields = ('nama',)

class ClosingAdmin(admin.ModelAdmin):
    list_display = ('id', 'produk', 'customer', 'qty', 'payment_method', 'total_transaksi')  # Menambahkan 'customer'

admin.site.register(Closing, ClosingAdmin)