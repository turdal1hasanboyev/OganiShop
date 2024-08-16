from apps.blog.models import Tag, Blog, Category


def blog_contexts(request):
    tags = Tag.objects.all()
    recent_blogs = Blog.objects.all()
    categories = Category.objects.all()

    return {
        'tags': tags.order_by('name'),
        'recent_blogs': recent_blogs.order_by('-id')[:3],
        'category': categories.order_by('name'),
    }
