from django.contrib import admin

from .forms import BlogAdminForm
from .models import Blog, Category, Tag


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    list_display = ['id', 'name', 'category', 'created_at']


admin.site.register(Category)
admin.site.register(Tag)
