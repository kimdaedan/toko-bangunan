from rest_framework import serializers
from .models import Pengeluaran

class PengeluaranSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pengeluaran
        fields = '__all__'  # Atau tentukan field yang ingin ditampilkan