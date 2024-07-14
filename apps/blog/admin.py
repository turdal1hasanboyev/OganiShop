from django.contrib import admin
from apps.blog.forms import BlogAdminForm
from apps.blog.models import Blog, Category, Tag


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    list_display = ['id', 'name', 'category', 'created_at']


admin.site.register(Category)
admin.site.register(Tag)
