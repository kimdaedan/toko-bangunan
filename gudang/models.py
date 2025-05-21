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
    nama = models.CharField(max_length=100, default="Pengeluaran Umum")  # Tambahkan default
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    tanggal = models.DateField()
    jumlah = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nama} - {self.tanggal}"