from django.db.models import Q

from apps.product.models import Category, Product
from apps.order.models import WishList, CartItem, Cart


def objects(request):
    categories = Category.objects.all()

    wishlist_count = 0
    
    cart = Cart.objects.filter(session_id=request.session.session_key, is_completed=False).first()
    cart_items = CartItem.objects.filter(cart_id=cart.id, order=None).count()
    wishlist_count = WishList.objects.filter(Q(session_id=request.session.session_key)).count()
    
    if request.user.is_authenticated:
        wishlist_count = WishList.objects.filter(Q(user_id=request.user.id)).count()
    
    max_price = Product.objects.all().order_by('-price').first().price
    min_price = Product.objects.all().order_by('price').first().price

    return {
        "categories": categories.order_by('name'),
        "wishlist_count": wishlist_count,
        "max_price": int(max_price),
        "min_price": int(min_price),
        "cart_total": cart.total if cart else 0,
        "cart_items_count": cart_items
    }
