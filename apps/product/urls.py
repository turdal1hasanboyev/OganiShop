from django.urls import path

from .views import index, shop_detail, shop


urlpatterns = [
    path('', index, name='index'),
    path('shop-detail/<slug:slug>/', shop_detail, name="detail"),
    path('shop/', shop, name="shop"),
]
