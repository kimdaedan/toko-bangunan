from django.db import models

class Customer(models.Model):
    nama = models.CharField(max_length=100)
    alamat = models.TextField()
    no_telepon = models.CharField(max_length=15)

    def __str__(self):
        return self.nama