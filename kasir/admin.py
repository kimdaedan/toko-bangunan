from django.contrib import admin
from .models import Customer, Transaksi
from gudang.models import Produk

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('nama', 'alamat', 'no_telepon')
    search_fields = ('nama',)  # Menambahkan pencarian berdasarkan nama

@admin.register(Transaksi)
class TransaksiAdmin(admin.ModelAdmin):
    list_display = ('customer', 'produk', 'metode_pembayaran', 'jumlah', 'tanggal')
    list_filter = ('metode_pembayaran', 'tanggal')
    search_fields = ('customer__nama', 'produk__nama')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['customer'].queryset = Customer.objects.all()
        form.base_fields['produk'].queryset = Produk.objects.all()
        return form