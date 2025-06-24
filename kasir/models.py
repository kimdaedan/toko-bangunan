from django.db import models
from gudang.models import Produk

class Customer(models.Model):
    nama = models.CharField(max_length=100)
    alamat = models.CharField(max_length=255)
    no_telepon = models.CharField(max_length=15)

    def __str__(self):
        return self.nama


class Transaksi(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    metode_pembayaran = models.CharField(max_length=50)
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transaksi {self.id} - {self.customer.nama}'

    def total_harga(self):
        return sum(item.subtotal for item in self.items.all())


class ItemTransaksi(models.Model):
    transaksi = models.ForeignKey(Transaksi, related_name='items', on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField(default=1)
    harga_satuan = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Hitung subtotal sebelum menyimpan
        self.subtotal = self.jumlah * self.harga_satuan
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Item {self.id} - {self.produk.nama}'