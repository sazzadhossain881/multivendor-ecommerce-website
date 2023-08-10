"""views for the product api"""

from rest_framework.views import APIView
from rest_framework.response import Response
from base.models import (
    Product,
)
from base.serializers import ProductSerializer


class ProductListView(APIView):
    def get(self, request):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class ProductRetrieveUpdateDeleteView(APIView):
    
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error':'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    
    def put(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)