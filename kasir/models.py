from django.db import models
from gudang.models import Produk

class Customer(models.Model):
    nama = models.CharField(max_length=100)
    alamat = models.CharField(max_length=255)
    no_telepon = models.CharField(max_length=15)

    def __str__(self):
        return self.nama

class Closing(models.Model):
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    qty = models.IntegerField()
    payment_method = models.CharField(max_length=100)
    total_transaksi = models.DecimalField(max_digits=10, decimal_places=2)
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Closing {self.id}"

# --- TAMBAHKAN KELAS BARU DI BAWAH INI ---
class Expense(models.Model):
    date = models.DateField()
    category = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, default='paid') # Contoh: 'paid' atau 'unpaid'

    def __str__(self):
        return f"{self.category} - {self.amount}"

    class Meta:
        ordering = ['-date']
