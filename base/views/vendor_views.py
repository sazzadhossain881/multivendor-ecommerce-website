"""views for the vendor api"""

from rest_framework.views import APIView
from base.serializers import (
    VendorSerializer,
)
from base.models import (
    Vendor,
)
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework import status


class VendorListView(APIView):
    """vendor list view"""
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        vendor = Vendor.objects.all()
        serializer = VendorSerializer(vendor, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class VendorDetailView(APIView):
    """vendor detail view"""
    def get(self, reqeust, pk):
        try:
            vendor = Vendor.objects.get(pk=pk)
        
        except Vendor.DoesNotExist:
            return Response({'error':'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = VendorSerializer(vendor, many=False)
        return Response(serializer.data)
    
    def put(self, request, pk):
        vendor = Vendor.objects.get(pk=pk)
        serializer = VendorSerializer(vendor, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        vendor = Vendor.objects.get(pk=pk)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
