"""views for the customer api"""

from rest_framework.views import APIView
from base.serializers import CustomerSerializer, CustomerAddressSerializer
from base.models import (
    Customer,
    CustomerAddress,
    User,
)
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


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
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

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


class CustomerAddressCreateListApiView(APIView):
    def get(self, request):
        address = CustomerAddress.objects.all()
        serializer = CustomerAddressSerializer(address, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerAddressSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class CustomerAddressRetrieveUpdateDeleteApiView(APIView):
    def get(self, request, pk):
        try:
            address = CustomerAddress.objects.get(pk=pk)

        except CustomerAddress.DoesNotExist:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerAddressSerializer(address, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        address = CustomerAddress.objects.get(pk=pk)
        serializer = CustomerAddressSerializer(address, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = CustomerAddress.objects.get(pk=pk)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @csrf_exempt
# def customer_login(request):
#     # msg = {"bool": True, "post": request.POST}
#     email = request.POST.get("email")
#     password = request.POST.get("password")
#     user = authenticate(email=email, password=password)
#     if user:
#         msg = {"bool": True, "user": user.email}
#     else:
#         msg = {"bool": False, "msg": "invalid email/password!"}
#     return JsonResponse(msg)


@csrf_exempt
def customer_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if email and password:
            user = authenticate(request, email=email, password=password)

            if user is not None:
                msg = {"bool": True, "user": user.email}
            else:
                msg = {"bool": False, "msg": "Invalid email/password!"}
        else:
            msg = {"bool": False, "msg": "Email and password are required."}
    else:
        msg = {"bool": False, "msg": "Invalid request method."}

    return JsonResponse(msg)


@csrf_exempt
def customer_register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        mobile = request.POST.get("mobile")

        if name and email and password:
            user = User.objects.create_user(name=name, email=email, password=password)

            if user is not None:
                user.save()
                customer = Customer.objects.create(user=user, mobile=mobile)
                msg = {
                    "bool": True,
                    "user": user.id,
                    "customer": customer.id,
                    "msg": "Thank you for your registration.You can login now.",
                }
            else:
                msg = {"bool": False, "msg": "Oops... something went wrong"}
        else:
            msg = {"bool": False, "msg": "Name, email, and password are required."}
    else:
        msg = {"bool": False, "msg": "Invalid request method."}

    return JsonResponse(msg)
