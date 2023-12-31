"""Django admin customization"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


from base import models


class UserAdmin(BaseUserAdmin):
    """Define the admin page for user"""

    ordering = ["id"]
    list_display = ["email", "name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("permission"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    readonly_fields = ["id"]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Vendor)
admin.site.register(models.Category)
# admin.site.register(models.Product)
admin.site.register(models.Customer)
admin.site.register(models.Order)
admin.site.register(models.OrderItems)
admin.site.register(models.CustomerAddress)
admin.site.register(models.Review)
admin.site.register(models.ProductImage)


class ProductImageInline(admin.StackedInline):
    model = models.ProductImage


class ProductAdmin(admin.ModelAdmin):
    # prepopulated_fields = {
    #     "slug": {
    #         "title",
    #     }
    # }
    inlines = [ProductImageInline]


admin.site.register(models.Product, ProductAdmin)


# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = "__all__"


# admin.site.register(models.OrderItems, OrderItemAdmin)
class WishListAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "customer"]


admin.site.register(models.WishList, WishListAdmin)
