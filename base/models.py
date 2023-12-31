from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from django.conf import settings


# Create your models here.
class UserProfileManager(BaseUserManager):
    """manage user in the system"""

    def create_user(self, email, name, password=None):
        """create user in the system"""
        if not email:
            raise ValueError("user must have an email address")
        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """create a superuser in the system"""
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """user in the system"""

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def get_full_name(self):
        """retrieve full name of the user"""
        return self.name

    def get_short_name(self):
        """retrieve short name of the user"""
        return self.name

    def __str__(self):
        """string representation of the user"""
        return self.email


class Vendor(models.Model):
    """vendor objects"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    address = models.TextField(null=True)

    class Meta:
        verbose_name_plural = "1.Vendors"

    def __str__(self):
        return self.user.name


class Category(models.Model):
    """category objects"""

    title = models.CharField(max_length=100)
    detail = models.TextField(null=True)

    class Meta:
        verbose_name_plural = "2.Categories"

    def __str__(self):
        return self.title


class Product(models.Model):
    """product objects"""

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="category",
    )
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    color = models.JSONField(null=True)
    detail = models.TextField(null=True)
    tags = models.TextField(null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)

    class Meta:
        verbose_name_plural = "3.Products"

    def __str__(self):
        return self.title

    def tag_list(self):
        if self.tags:
            tagList = self.tags.split(",")
            return tagList
        else:
            return []


class Customer(models.Model):
    """customer objects"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    mobile = models.PositiveIntegerField(unique=True)

    class Meta:
        verbose_name_plural = "4.Customers"

    def __str__(self):
        return self.user.name


class Order(models.Model):
    """order objects"""

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
    )
    order_status = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "5.Orders"


class OrderItems(models.Model):
    """orderItems object"""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=True,
        related_name="order_items",
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = "6.OrderItems"

    def __str__(self):
        return self.product.title


class CustomerAddress(models.Model):
    """customer address objects"""

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="customer_address",
        null=True,
    )
    address = models.TextField()

    class Meta:
        verbose_name_plural = "7.CustomerAddresses"


class Review(models.Model):
    """review objects"""

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="review_customers"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="review_products"
    )
    rating = models.IntegerField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "8.Reviews"

    def __str__(self):
        return f"{self.rating} - {self.review}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_image"
    )
    image = models.ImageField(null=True)

    def __str__(self):
        return self.image.url


class WishList(models.Model):
    """wishlist objects"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "WishList"

    def __str__(self):
        return f"{self.product.title} - {self.customer.user.name}"
