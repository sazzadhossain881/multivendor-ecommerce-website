"""views for the product api"""

from rest_framework.views import APIView
from rest_framework.response import Response
from base.models import Product, Review, Category, WishList, Customer

from base.serializers import (
    ProductSerializer,
    ReviewSerializer,
    CategorySerializer,
    WishListSerializer,
)
from rest_framework import pagination
from rest_framework import status
from rest_framework import generics

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


class ProductListView(APIView):
    pagination_class = pagination.PageNumberPagination

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
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

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


class ReviewCreateListApiView(APIView):
    def get(self, request):
        review = Review.objects.all()
        serializer = ReviewSerializer(review, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ReviewRetrieveUpadateDeleteApiView(APIView):
    def get(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReviewSerializer(review, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        review = Review.objects.get(pk=pk)
        serializer = ReviewSerializer(review, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        review = Review.objects.get(pk=pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListCreateApiView(APIView):
    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class CategoryRetrieveUpdateDeleteApiView(APIView):
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RelatedProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        qs = qs.filter(category=product.category).exclude(id=product_id)
        return qs


class WishListListCreateView(generics.ListCreateAPIView):
    """wishList list create api view"""

    serializer_class = WishListSerializer
    queryset = WishList.objects.all()


@csrf_exempt
def check_in_wish_list(request):
    if request.method == "POST":
        product_id = request.POST.get("product")
        customer_id = request.POST.get("customer")

        # product = Product.objects.get(id = product_id)
        # customer = Customer.objects.get(id = customer_id)
        checkWishList = WishList.objects.filter(
            product__id=product_id, customer__id=customer_id
        ).count()

        msg = {"bool": False}
        if checkWishList > 0:
            msg = {"bool": True}

    return JsonResponse(msg)


@csrf_exempt
def remove_from_wishlist(request):
    if request.method == "POST":
        wishlist_id = reqquest.POST.get("wishlist_id")
        res = WishList.objects.filter(id=wishlist_id).delete()

        msg = {"bool": False}

        if res:
            msg = {"bool": True}

    return JsonResponse(msg)


class CustomerWishItemListView(generics.ListAPIView):
    """customer wish item list view"""

    serializer_class = WishListSerializer
    queryset = WishList.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        customer_id = self.kwargs["pk"]
        qs = qs.filter(customer__id=customer_id)
        return qs
