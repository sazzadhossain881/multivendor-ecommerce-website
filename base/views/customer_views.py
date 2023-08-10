"""views for the customer api"""

from rest_framework.views import APIView
from base.serializers import (
    CustomerSerializer,
)
from base.models import (
    Customer
)
from rest_framework.response import Response
from rest_framework import status


class CustomerCreateListApiView(APIView):

    def get(self, request):
        customer = Customer.objects.all()
        serializer = CustomerSerializer(customer, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class CustomerRetrieveUpdateDeleteApiView(APIView):

    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({'error':'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CustomerSerializer(customer, many=False)
        return Response(serializer.data)
    
    def post(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        serializer = CustomerSerializer(customer, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)