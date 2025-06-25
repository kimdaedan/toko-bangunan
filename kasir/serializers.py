from rest_framework import serializers
from .models import Customer, Closing  # Hanya Customer dan Closing
from gudang.models import Produk

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'nama', 'alamat', 'no_telepon']

class ClosingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Closing
        fields = '__all__'