"""views for the order api"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from base.serializers import (
    OrderSerializer,
    OrderDetailSerializer
)
from base.models import (
    Order,
    OrderItems
)
from rest_framework import generics


class OrderListCreateApiView(APIView):

    def get(self, request):
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class OrderDetailApiView(generics.ListAPIView):

    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        order_id = self.kwargs['pk']
        order = Order.objects.get(id=order_id)
        order_items = OrderItems.objects.filter(order=order)
        return order_items