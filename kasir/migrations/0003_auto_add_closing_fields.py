from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gudang', '0001_initial'),  # Sesuaikan dengan migrasi awal model Produk
        ('kasir', '0001_initial'),   # Sesuaikan dengan migrasi awal model Customer jika ada
    ]

    operations = [
        migrations.CreateModel(
            name='Closing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),  # Jumlah produk
                ('payment_method', models.CharField(max_length=100)),  # Metode pembayaran
                ('total_transaksi', models.DecimalField(max_digits=10, decimal_places=2)),  # Total transaksi
                ('customer', models.ForeignKey(to='kasir.Customer', on_delete=models.CASCADE)),  # ForeignKey ke Customer
                ('produk', models.ForeignKey(to='gudang.Produk', on_delete=models.CASCADE)),  # ForeignKey ke Produk
            ],
        ),
    ]