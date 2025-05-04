from rest_framework import viewsets
from django.shortcuts import render, redirect
from .models import Produk
from .serializers import ProdukSerializer

class ProdukViewSet(viewsets.ModelViewSet):
    queryset = Produk.objects.all()
    serializer_class = ProdukSerializer

def tambah_produk(request):
    if request.method == 'POST':
        form_data = {
            'nama': request.POST.get('nama'),
            'deskripsi': request.POST.get('deskripsi'),
            'harga': request.POST.get('harga'),
            'stok': request.POST.get('stok'),
            'gambar': request.FILES.get('gambar'),
        }
        serializer = ProdukSerializer(data=form_data)
        if serializer.is_valid():
            serializer.save()
            return redirect('tambah_produk')  # Ganti dengan URL yang diinginkan setelah sukses
    return render(request, 'produk/form_produk.html')