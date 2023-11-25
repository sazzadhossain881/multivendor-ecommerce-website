"""url mapping for the order api view"""

from django.urls import path
from base.views import order_views as views


urlpatterns = [
    path("", views.OrderListCreateApiView.as_view(), name="order-list"),
    path("list/", views.OrderItemListApiView.as_view(), name="order-item-list"),
    path("<str:pk>/", views.OrderDetailApiView.as_view(), name="order-detail"),
    path(
        "update-order-status/<str:pk>/",
        views.update_order_status,
        name="update-order-status",
    ),
    path("customer/<str:pk>/order_items/", views.CustomerOrderItemList.as_view(), name='customer-order-item-list'),
]
