from django.urls import path
from apps.product.views import index, shop_detail, shop
from apps.blog.views import blog_detail


urlpatterns = [
    path('', index, name='index'),
    path('shop-detail/<slug:slug>/', shop_detail, name="detail"),
    path('blog-detail/<slug:slug>/', blog_detail, name='blog-detail'),
    path('shop/', shop, name="shop"),
]
