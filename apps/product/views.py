from django.shortcuts import render, redirect

from django.db.models import Q
from django.core.paginator import Paginator

from .models import Banner, Category, Product
from apps.blog.models import Blog
from apps.common.models import SubEmail


def index(request):
    search = request.GET.get('query')

    cat = request.GET.get('cat')

    banners = Banner.objects.all()
    blogs = Blog.objects.all()
    categories = Category.objects.all()
    products = Product.objects.all()

    parent = banners.filter(parent__isnull=True).last()

    last_products = products.order_by('-id')
    top_reted_products = products.order_by('-id')
    review_products = products.order_by('-id')
    
    if cat:
        products = products.filter(category__slug__exact=cat)

    if request.method == "POST":
        sub_email = request.POST.get("subemail")

        SubEmail.objects.create(
            sub_email=sub_email,
        )

        return redirect ('index')

    context = {
        'banner': parent,
        'last_two_banners': banners.filter(parent=parent),
        'categories': categories.order_by('name'), 
        'products': products.order_by('?')[:9],
        'last_products': last_products[:6],
        'top_reted_products': top_reted_products[:6],
        'review_products': review_products[:6],
        'blogs': blogs[:3]
    }

    return render(request, 'index.html', context)

def shop(request):
    min_price = request.GET.get('min', None)
    max_price = request.GET.get('max', None)

    cat = request.GET.get('cat')
    page = request.GET.get('page')

    search = request.GET.get('query')

    products = Product.objects.all()
    
    sale_products = products.order_by('-percentage').exclude(Q(percentage=None) | Q(percentage=0))
    last_products = products.order_by('-id')

    paginator = Paginator(products, 3)
    selected_page = paginator.get_page(page)

    if max_price and min_price:
        products = Product.objects.filter(price__gte=float(min_price.strip('$')), price__lte=float(max_price.strip('$')))

    if cat:
        products = products.filter(category__slug__exact=cat)

    if request.method == "POST":
        sub_email = request.POST.get("subemail")
        
        SubEmail.objects.create(
            sub_email=sub_email,
        )

        return redirect ('shop')

    context = {
        'products': products.order_by('?')[:9],
        'sale_products': sale_products[:6],
        'object_list': selected_page,
        'last_products': last_products[:6],
    }

    return render(request, 'shop.html', context)

def shop_detail(request, slug):
    cat = request.GET.get('cat')
    search = request.GET.get('query')

    product = Product.objects.filter(slug__iexact=slug).first()
    related_products = Product.objects.filter(category_id=product.category.id).exclude(id=product.id)

    if request.method == "POST":
        sub_email = request.POST.get("subemail")

        SubEmail.objects.create(
            sub_email=sub_email,
        )

        return redirect('shop-detail', product.slug)

    context = {
        'product': product,
        'related_products': related_products[:4],
    }

    return render(request, 'detail.html', context)
