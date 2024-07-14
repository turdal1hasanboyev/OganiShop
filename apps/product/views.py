from django.shortcuts import render, redirect
from apps.product.models import Banner, Category, Product
from apps.blog.models import Blog
from django.db.models import Q
from django.core.paginator import Paginator
from apps.common.models import SubEmail


def index(request):
    search = request.GET.get('query')
    cat = request.GET.get('cat')

    banners = Banner.objects.all()
    parent = banners.filter(parent__isnull=True).last()
    categories = Category.objects.all().order_by('name')
    products = Product.objects.all()
    last_products = products.order_by('-id')[:6]
    top_reted_products = products.order_by('-id')[:6]
    review_products = products.order_by('-id')[:6]
    blogs = Blog.objects.all()

    if cat:
        products = products.filter(category__slug__exact=cat)

    if request.method == "POST":
        email = request.POST.get("subemail")
        SubEmail.objects.create(
            email=email,
        )

        return redirect ('index')

    context = {
        'banner': parent,
        'last_two_banners': banners.filter(parent=parent),
        'categories': categories, 
        'products': products.order_by('?')[:9],
        'last_products': last_products,
        'top_reted_products': top_reted_products,
        'review_products': review_products,
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
    sale_products = products.order_by('-percentage').exclude(Q(percentage=None) | Q(percentage=0))[:6]
    last_products = products.order_by('-id')[:6]

    paginator = Paginator(products, 3)
    selected_page = paginator.get_page(page)

    if max_price and min_price:
        products = Product.objects.filter(price__gte=float(min_price.strip('$')), price__lte=float(max_price.strip('$')))

    if cat:
        products = products.filter(category__slug__exact=cat)

    if request.method == "POST":
        email = request.POST.get("subemail")
        SubEmail.objects.create(
            email=email,
        )

        return redirect ('shop')

    context = {
        'products': products.order_by('?')[:9],
        'sale_products': sale_products,
        'object_list': selected_page,
        'last_products': last_products,
    }

    return render(request, 'shop.html', context)

def shop_detail(request, slug):
    cat = request.GET.get('cat')
    search = request.GET.get('query')

    product = Product.objects.filter(slug__iexact=slug).first()

    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    if request.method == "POST":
        email = request.POST.get("subemail")
        SubEmail.objects.create(
            email=email,
        )

        return redirect('shop-detail', product.slug)

    context = {
        'product': product,
        'related_products': related_products,
    }

    return render(request, 'detail.html', context)
