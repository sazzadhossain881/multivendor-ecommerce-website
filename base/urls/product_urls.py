"""mapping url for the product api view"""

from django.urls import path
from base.views import product_views as views

urlpatterns = [
    path("list/", views.ProductListView.as_view(), name="product-list"),
    path(
        "list/<str:pk>/",
        views.ProductRetrieveUpdateDeleteView.as_view(),
        name="product-retrieve-update-delete",
    ),
    path("review/", views.ReviewCreateListApiView.as_view(), name="review-list"),
    path(
        "review/<str:pk>/",
        views.ReviewRetrieveUpadateDeleteApiView.as_view(),
        name="review-retrieve-update-delete",
    ),
    path("category/", views.CategoryListCreateApiView.as_view(), name="category-list"),
    path(
        "category/<str:pk>/",
        views.CategoryRetrieveUpdateDeleteApiView.as_view(),
        name="category-retrieve-update-delete",
    ),
    path(
        "related-product/<str:pk>/",
        views.RelatedProductView.as_view(),
        name="related-product",
    ),
]
