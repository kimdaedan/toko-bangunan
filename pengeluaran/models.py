from django.db import models

class Kategori(models.Model):
    nama = models.CharField(max_length=50)

    def __str__(self):
        return self.nama

class Pengeluaran(models.Model):
    tanggal = models.DateField()
    nama_pengeluaran = models.CharField(max_length=100)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    jumlah = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nama_pengeluaran} - {self.tanggal}"