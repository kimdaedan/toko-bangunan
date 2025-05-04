from rest_framework import viewsets
from django.shortcuts import render, redirect
from .models import Pengeluaran, Kategori
from .serializers import PengeluaranSerializer

class PengeluaranViewSet(viewsets.ModelViewSet):
    queryset = Pengeluaran.objects.all()
    serializer_class = PengeluaranSerializer

def tambah_pengeluaran(request):
    if request.method == 'POST':
        # Get data from the form
        form_data = {
            'tanggal': request.POST.get('tanggal'),
            'nama_pengeluaran': request.POST.get('nama_pengeluaran'),
            'kategori': request.POST.get('kategori'),  # This should be the ID of the Kategori
            'jumlah': request.POST.get('jumlah'),
        }

        # Create serializer instance
        serializer = PengeluaranSerializer(data=form_data)

        if serializer.is_valid():
            serializer.save()
            return redirect('pengeluaran-list')
        else:
            # Handle the case where serializer is not valid
            return render(request, 'pengeluaran/form_pengeluaran.html', {
                'kategoris': Kategori.objects.all(),
                'errors': serializer.errors,  # Pass the errors to the template
                'form_data': form_data         # Retain input data
            })

    # If GET request, render the form with categories
    kategoris = Kategori.objects.all()
    return render(request, 'pengeluaran/form_pengeluaran.html', {'kategoris': kategoris})