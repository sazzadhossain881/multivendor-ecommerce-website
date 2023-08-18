"""url mapping for the customer api view"""

from django.urls import path
from base.views import customer_views as views


urlpatterns = [
    path('list/', views.CustomerCreateListApiView.as_view(), name='customer-list'),
    path('list/<str:pk>/', views.CustomerRetrieveUpdateDeleteApiView.as_view(), name='customer-retrieve-update-delete'),
    path('address/', views.CustomerAddressCreateListApiView.as_view(), name='customer-address-list'),
    # path('addresses/<str:pk>/', views.CustomerAddressRetrieveUpdateDeleteApiView.as_view(), name='customer-address-retrieve-update-delete'),
    
]
