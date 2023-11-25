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
    path(
        "wishList/list/",
        views.WishListListCreateView.as_view(),
        name="wish-list-list-create-view",
    ),
    # path("check-in-wishList/", views.   , name='check-in-wishList'),
    path("check-in-wishList/", views.check_in_wish_list, name="check-in-wishList"),
    path("remove-from-wishlist/", views.remove_from-wishlist, name='remove-from-wishlist'),
    path(
        "customer/<str:pk>/wishItems/",
        views.CustomerWishItemListView.as_view(),
        name="customer-wish-item-list-view",
    ),
]
