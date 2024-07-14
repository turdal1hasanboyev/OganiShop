from django.contrib import admin
from apps.product.models import Banner, Category, Tag, Product, ProductImage, Rate


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['name', 'price', 'category', 'percentage']
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Banner)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(ProductImage)
admin.site.register(Rate)
