from rest_framework import serializers
from base.models import (
    Vendor,
    Product,
    User,
    Customer,
    Order,
    OrderItems,
    CustomerAddress,
    Review,
    Category,
    ProductImage,
    WishList,
)

from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    """serializer for the user"""

    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "name", "email", "isAdmin"]

    def get_isAdmin(self, obj):
        return obj.is_staff


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "name", "email", "isAdmin", "token"]
        extra_kwargs = {
            "token": {
                "read_only": True,
            }
        }

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class VendorSerializer(serializers.ModelSerializer):
    """serializer for the vendor objects"""

    class Meta:
        model = Vendor
        fields = ["id", "user", "address"]

    def __init__(self, *args, **kwargs):
        super(VendorSerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth=1


class ProductImageSerializer(serializers.ModelSerializer):
    """serializer for the product image"""

    class Meta:
        model = ProductImage
        fields = ["id", "product", "image"]


class ProductSerializer(serializers.ModelSerializer):
    """serializer for the product object"""

    review_products = serializers.StringRelatedField(many=True, read_only=True)
    product_image = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "vendor",
            "title",
            "color",
            "detail",
            "price",
            "tag_list",
            "review_products",
            "product_image",
        ]

    def __init__(self, *args, **kwargs):
        super(ProductSerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth=1


class CustomerSerializer(serializers.ModelSerializer):
    """serializer for the customer objects"""

    class Meta:
        model = Customer
        fields = ["id", "user", "mobile"]

    def __init__(self, *args, **kwargs):
        super(CustomerSerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth = 1


class OrderSerializer(serializers.ModelSerializer):
    """serializer for the order objects"""

    class Meta:
        model = Order
        fields = ["id", "customer"]

    def __init__(self, *args, **kwargs):
        super(OrderSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


class OrderDetailSerializer(serializers.ModelSerializer):
    """serializer for the order items objects"""

    # order = OrderSerializer()
    # product = ProductSerializer()
    class Meta:
        model = OrderItems
        fields = ["id", "order", "product", "quantity", "price"]

    # def __init__(self, *args, **kwargs):
    #     super(OrderDetailSerializer, self).__init__(*args, **kwargs)
    #     self.Meta.depth = 1

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["order"] = OrderSerializer(instance.order).data
        reaponse["product"] = ProductSerializer(instance.product).data
        return response


class CustomerAddressSerializer(serializers.ModelSerializer):
    """serilizer for the customer address objects"""

    class Meta:
        model = CustomerAddress
        fields = ["id", "customer", "address"]

    def __init__(self, *args, **kwargs):
        super(CustomerAddressSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "customer", "product", "rating", "review", "created_at"]

    def __init__(self, *args, **kwargs):
        super(ReviewSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


class CategorySerializer(serializers.ModelSerializer):
    """serializer for the category objects"""

    class Meta:
        model = Category
        fields = ["id", "title", "description"]

    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


class WishListSerializer(serializers.ModelSerializer):
    """serializer for the wishList objects"""

    class Meta:
        model = WishList
        fields = ["id", "product", "customer"]

    def __init__(self, *args, **kwargs):
        super(WishListSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["customer"] = CustomerSerializer(instance.customer).data
        response["product"] = ProductSerializer(instance.product).data
        return response
