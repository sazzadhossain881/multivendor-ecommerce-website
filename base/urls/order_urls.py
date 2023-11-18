"""url mapping for the order api view"""

from django.urls import path
from base.views import order_views as views


urlpatterns = [
    path('', views.OrderListCreateApiView.as_view(), name='order-list'),
    path('<str:pk>/', views.OrderDetailApiView.as_view(), name='order-detail'),
]
