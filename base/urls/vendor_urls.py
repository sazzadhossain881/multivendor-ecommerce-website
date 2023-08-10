from django.urls import path
from base.views import vendor_views as views


urlpatterns = [
    path('', views.VendorListView.as_view(), name='vendor-list'),
    path('<str:pk>/', views.VendorDetailView.as_view(), name='vendor-detail'),
]
