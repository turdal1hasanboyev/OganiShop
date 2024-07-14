from apps.blog.models import Tag, Blog, Category


def blog_contexts(request):
    tags = Tag.objects.all().order_by('name')
    recent_blogs = Blog.objects.all().order_by('-id')[:3]
    categories = Category.objects.all().order_by('name')

    return {
        'tags': tags,
        'recent_blogs': recent_blogs,
        'category': categories,
    }
