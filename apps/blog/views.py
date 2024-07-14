from django.shortcuts import render, redirect
from apps.blog.models import Category, Tag, Blog
from django.core.paginator import Paginator
from apps.common.models import SubEmail


def blog(request):
    page = request.GET.get('page')
    tag = request.GET.get('tag')
    cat = request.GET.get('cat')
    search = request.GET.get('query')

    blogs = Blog.objects.all()

    if request.method == "POST":
        email = request.POST.get("subemail")
        SubEmail.objects.create(
            email=email,
        )

        return redirect ('blog')

    if tag:
        blogs = blogs.filter(tags__slug__exact=tag)

    if cat:
        blogs = blogs.filter(category__slug__exact=cat)

    paginator = Paginator(blogs, 3)
    selected_page = paginator.get_page(page)

    context = {
        'blogs': selected_page,
    }

    return render(request, 'blog.html', context)

def blog_detail(request, slug):
    tag = request.GET.get('tag')
    cat = request.GET.get('cat')
    search = request.GET.get('query')

    blog = Blog.objects.get(slug__exact=slug)

    blogs = Blog.objects.all().order_by('-id')[:3]

    if request.method == "POST":
        email = request.POST.get("subemail")
        SubEmail.objects.create(
            email=email,
        )

        return redirect ('blog', blog.slug)

    if tag:
        blogs = blogs.filter(tags__slug__exact=tag)

    if cat:
        blogs = blogs.filter(category__slug__exact=cat)

    context = { 
        'blog': blog,
        'blogs': blogs,
    }

    return render(request, 'blog-detail.html', context)
