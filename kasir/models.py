from django.db import models
from gudang.models import Produk

class Customer(models.Model):
    nama = models.CharField(max_length=100)
    alamat = models.CharField(max_length=255)
    no_telepon = models.CharField(max_length=15)

    def __str__(self):
        return self.nama

class Closing(models.Model):
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)  # ForeignKey ke Produk
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    qty = models.IntegerField()  # Jumlah produk
    payment_method = models.CharField(max_length=100)  # Metode pembayaran
    total_transaksi = models.DecimalField(max_digits=10, decimal_places=2)  # Total transaksi
    tanggal = models.DateTimeField(auto_now_add=True)  # Tanggal otomatis

    def __str__(self):
        return f"Closing {self.id}: Total: {self.total_transaksi:.2f} IDR"