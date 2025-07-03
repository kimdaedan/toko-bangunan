from django.db import models

class Kategori(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama

class Produk(models.Model):
    nama = models.CharField(max_length=100)
    jumlah = models.IntegerField()
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    gambar = models.ImageField(upload_to='produk/', null=True)

    def __str__(self):
        return self.nama

class Pengeluaran(models.Model):
    # Cek nama field yang sebenarnya ada di model
    # Contoh:
    name = models.CharField(default='Untitled', max_length=100)
    date = models.DateTimeField(auto_now_add=True)# mungkin 'date' bukan 'tanggal'
    category = models.CharField(max_length=100, default='uncategorized')  # mungkin 'category' bukan 'kategori'
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(
        max_length=20,
        choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')],
        default='unpaid'
    )
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date']


