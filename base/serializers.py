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
)

from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    """serializer for the user"""
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'isAdmin']

    def get_isAdmin(self, obj):
        return obj.is_staff


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'isAdmin', 'token']
        extra_kwargs = {
            'token': {
                'read_only': True,
            }
        }

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

class VendorSerializer(serializers.ModelSerializer):
    """serializer for the vendor objects"""
    class Meta:
        model = Vendor
        fields = ['id','user', 'address']

    def __init__(self, *args, **kwargs):
        super(VendorSerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth=1

class ProductSerializer(serializers.ModelSerializer):
    """serializer for the product object"""
    review_products = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id','category', 'vendor', 'title', 'detail', 'price', 'review_products']

    def __init__(self, *args, **kwargs):
        super(ProductSerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth=1

class CustomerSerializer(serializers.ModelSerializer):
    """serializer for the customer objects"""
    class Meta:
        model = Customer
        fields = ['id', 'user', 'mobile']

    def __init__(self, *args, **kwargs):
        super(CustomerSerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth = 1

class OrderSerializer(serializers.ModelSerializer):
    """serializer for the order objects"""
    class Meta:
        model = Order
        fields = ['id', 'customer']

    def __init__(self, *args, **kwargs):
        super(OrderSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth=1

class OrderDetailSerializer(serializers.ModelSerializer):
    """serializer for the order items objects"""
    class Meta:
        model = OrderItems
        fields = ['id', 'order', 'product']
    
    def __init__(self, *args, **kwargs):
        super(OrderDetailSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth=1
    
class CustomerAddressSerializer(serializers.ModelSerializer):
    """serilizer for the customer address objects"""
    class Meta:
        model = CustomerAddress
        fields = ['id','customer', 'address']
    
    def __init__(self, *args, **kwargs):
        super(CustomerAddressSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth=1

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','customer', 'product', 'rating', 'review', 'created_at']
    
    def __init__(self, *args, **kwargs):
        super(ReviewSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth=1

class CategorySerializer(serializers.ModelSerializer):
    """serializer for the category objects"""
    class Meta:
        model = Category
        fields = ['id','title', 'description']
    
    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)
        self.Meta.depth=1