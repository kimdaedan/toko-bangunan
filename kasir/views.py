from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Customer, Closing
from .serializers import CustomerSerializer, ClosingSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ClosingViewSet(viewsets.ModelViewSet):
    queryset = Closing.objects.all()
    serializer_class = ClosingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Menangani pembuatan objek
        try:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(serializer.data))
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)