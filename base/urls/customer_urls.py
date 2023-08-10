"""url mapping for the customer api view"""

from django.urls import path
from base.views import customer_views as views


urlpatterns = [
    path('', views.CustomerCreateListApiView.as_view(), name='customer-list'),
    path('<str:pk>/', views.CustomerRetrieveUpdateDeleteApiView.as_view(), name='customer-retrieve-update-delete'),
    
]
