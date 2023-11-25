"""views for the order api"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from base.serializers import OrderSerializer, OrderDetailSerializer
from base.models import Order, OrderItems
from rest_framework import generics
from django.http import JsonResponse


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


class OrderItemListApiView(APIView):
    def get(self, request):
        order_item = OrderItems.objects.all()
        serializer = OrderDetailSerializer(order_item, many=True)
        return Response(serializer.data)


class OrderDetailApiView(generics.ListAPIView):
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        order_id = self.kwargs["pk"]
        order = Order.objects.get(id=order_id)
        order_items = OrderItems.objects.filter(order=order)
        return order_items


def update_order_status(request, pk):
    if request.method == "POST":
        updateRes = Order.objects.filter(pk=pk).update(order_status=True)
        msg = {"bool": False}

        if updateRes:
            msg = {"bool": True}

    return JsonResponse(msg)

class CustomerOrderItemList(generics.ListAPIView):
    serializer_class = OrderDetailSerializer
    queryset = OrderItems.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        customer_id = self.kwargs['pk']
        qs = qs.filter(order__customer__id = customer_id)
        return qs