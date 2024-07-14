from django.urls import path
from .views import add_to_cart, add_to_wish_list, cart, remove_from_cart, create_order, checkout, wishlist, remove_from_wishlist


urlpatterns = [
    path('add_to_cart/', add_to_cart, name="add_to_cart"),
    path('add_wish-item/<int:pk>/', add_to_wish_list, name="add_to_wish_list"),
    path('my-cart/', cart, name="cart"),
    path('remove-from-cart/<int:pk>/', remove_from_cart, name="remove_from_cart"),
    path('create-order/', create_order, name="order"),
    path('checkout/', checkout, name="checkout"),
    path('wishlist/', wishlist, name="wishlist"),
    path('remove-from-wishlist/<int:pk>/', remove_from_wishlist, name="remove_from_wishtlist"),
]
