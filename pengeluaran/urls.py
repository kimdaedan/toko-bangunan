from django.urls import path
from .views import PengeluaranViewSet, tambah_pengeluaran

urlpatterns = [
    path('tambah/', tambah_pengeluaran, name='tambah_pengeluaran'),
    path('', PengeluaranViewSet.as_view({'get': 'list', 'post': 'create'}), name='pengeluaran-list'),
]