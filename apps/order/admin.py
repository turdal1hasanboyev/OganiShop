from django.contrib import admin

from apps.order.models import Order, Cart, CartItem, WishList


class CartItemInline(admin.TabularInline):
    readonly_fields = ('cart', 'product', 'quantity', 'total',)
    model = CartItem
    extra = 0


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    readonly_fields = ('total',)
    list_display = ('id', 'cart', 'quantity', 'total', 'product')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ('id', 'session_id', 'ip_address', 'total', 'main_total', 'items_count', 'is_completed')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ('id', 'status', 'user')
    readonly_fields = ('user', 'phone', 'full_name', 'notes', 'created_at', 'total')
    list_filter = ('status',)


admin.site.register(WishList)
