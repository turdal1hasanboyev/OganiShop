from django.urls import path

from .views import blog, blog_detail


urlpatterns = [
    path('blog/', blog, name='blog'),
    path('blog-detail/<slug:slug>/', blog_detail, name='blog-detail'),
]
