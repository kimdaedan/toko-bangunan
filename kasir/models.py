from django.db import models
from gudang.models import Produk

class Customer(models.Model):
    nama = models.CharField(max_length=100)
    alamat = models.CharField(max_length=255)
    no_telepon = models.CharField(max_length=15)

    def __str__(self):
        return self.nama  # Mengembalikan nama customer

class Transaksi(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    metode_pembayaran = models.CharField(max_length=50)
    jumlah = models.PositiveIntegerField()
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transaksi {self.id} - {self.customer.nama} - {self.jumlah} pcs'