"""mapping url for the product api view"""

from django.urls import path
from base.views import product_views as views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('<str:pk>/', views.ProductRetrieveUpdateDeleteView.as_view(), name='product-retrieve-update-delete'),
]

