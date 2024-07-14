from apps.product.models import Category, Product
from apps.order.models import WishList, CartItem, Cart
from django.db.models import Q


def objects(request):
    categories = Category.objects.all().order_by('name')
    wishlist_count = 0
    cart = Cart.objects.filter(session_id=request.session.session_key, is_completed=False).first()
    cart_items = CartItem.objects.filter(cart=cart, order=None, is_active=True).count()
    wishlist_count = WishList.objects.filter(Q(session_id=request.session.session_key)).count()
    
    if request.user.is_authenticated:
        wishlist_count = WishList.objects.filter(Q(user=request.user)).count()
    
    max_price = Product.objects.all().order_by('-price').first().price
    min_price = Product.objects.all().order_by('price').first().price

    return {
        "categories": categories,
        "wishlist_count": wishlist_count,
        "max_price": int(max_price),
        "min_price": int(min_price),
        "cart_total": cart.total if cart else 0,
        "cart_items_count": cart_items
    }
