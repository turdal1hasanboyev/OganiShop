from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required
from django.db.models import Q

from apps.product.models import Product
from .models import Cart, CartItem, WishList, Order
from apps.common.models import SubEmail


def add_to_cart(request):
    url = request.META.get('HTTP_REFERER')

    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')

    session_id = request.session.session_key

    ip_address = request.META.get('REMOTE_ADDR')

    cart = Cart.objects.filter(session_id=session_id, is_completed=False).first()

    product = Product.objects.get(id=int(product_id))

    if cart:
        cart_item = CartItem.objects.filter(cart_id=cart.id, product_id=product.id).first()

        if cart_item:
            cart_item.quantity = int(quantity)

            cart_item.save()

        else:
            CartItem.objects.create(cart_id=cart.id, product_id=product.id, quantity=quantity)

    else:
        cart = Cart.objects.create(session_id=session_id, ip_address=ip_address)

        CartItem.objects.create(cart_id=cart.id, product_id=product.id, quantity=quantity)

    return redirect(url)

def add_to_wish_list(request, pk):
    url = request.META.get('HTTP_REFERER')

    if request.user.is_authenticated:
        wishlist = WishList.objects.filter(product_id=pk, user_id=request.user.id).first()

        if wishlist:
            wishlist.delete()

        else:
            WishList.objects.create(product_id=pk, user_id=request.user.id)

    else:
        wishlist = WishList.objects.filter(product_id=pk, session_id=request.session.session_key).first()

        if wishlist:
            wishlist.delete()

        else:
            WishList.objects.create(product_id=pk, session_id=request.session.session_key)

    return redirect(url)

def cart(request):
    cat = request.GET.get('cat')
    search = request.GET.get('query')

    cart = Cart.objects.filter(session_id=request.session.session_key, is_completed=False).first()
    cart_items = CartItem.objects.filter(cart_id=cart.id, order=None)

    if request.method == "POST":
        sub_email = request.POST.get("subemail")

        SubEmail.objects.create(sub_email=sub_email)

        return redirect ('cart')

    context = {
        "cart": cart,
        "cart_items": cart_items,
    }

    return render(request, 'cart.html', context)

def remove_from_cart(request, pk):
    url = request.META.get('HTTP_REFERER')

    cart_item = CartItem.objects.get(id=pk)

    cart_item.delete()

    return redirect(url)

def remove_from_wishlist(request, pk):
    url = request.META.get('HTTP_REFERER')

    cart_item = WishList.objects.get(id=pk)

    cart_item.delete()
    
    return redirect(url)

@login_required
def create_order(request):
    cart = Cart.objects.filter(session_id=request.session.session_key, is_completed=False).first()
    cart_items = CartItem.objects.filter(cart_id=cart.id, order=None)

    order = Order.objects.create(user_id=request.user.id)

    for item in cart_items:
        item.order = order
        
        item.save()

    cart.is_completed = True

    cart.save()

    return redirect('checkout')

@login_required
def checkout(request):
    cat = request.GET.get('cat')
    search = request.GET.get('query')

    full_name = request.POST.get('full_name', None)
    phone = request.POST.get('phone', None)
    notes = request.POST.get('notes', None)

    order = Order.objects.filter(user_id=request.user.id).last()
    
    if request.method == 'POST':
        order.full_name = full_name
        order.phone = phone
        order.notes = notes
        
        order.save()

        return redirect('index')
    
    if request.method == "POST":
        sub_email = request.POST.get("subemail")

        SubEmail.objects.create(
            sub_email=sub_email,
        )

        return redirect ('checkout')

    return render(request, 'checkout.html', {"order": order})

def wishlist(request):
    cat = request.GET.get('cat')
    search = request.GET.get('query')

    wishlist = WishList.objects.filter(session_id=request.session.session_key)

    if request.user.is_authenticated:
        wishlist = WishList.objects.filter(Q(user_id=request.user.id) | Q(session_id=request.session.session_key))

    if request.method == "POST":
        sub_email = request.POST.get("subemail")
        
        SubEmail.objects.create(
            sub_email=sub_email,
        )

        return redirect ('wishlist')

    return render(request, 'wishlist.html', {"wishlist": wishlist})
