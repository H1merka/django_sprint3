from blog.models import Post, Category
from django.shortcuts import render, get_list_or_404, get_object_or_404
from datetime import datetime


'''
class BlogListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = '-pub_date'
    paginate_by = 5


class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
'''


# Create your views here.
def index(request):
    template_name = 'blog/index.html'
    post_list = Post.objects.select_related(
        'category',
        'author',
        'location'
    ).filter(
        is_published=True,
        pub_date__lte=datetime.now(),
        category__is_published=True
    ).order_by(
        '-pub_date'
    )[:5]
    context = {
        'post_list': post_list
    }
    return render(request, template_name, context)


def post_detail(request, id):
    template_name = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related(
            'category',
            'author',
            'location'
        ).filter(
            id=id,
            pub_date__lte=datetime.now(),
            is_published=True,
            category__is_published=True
        )
    )
    context = {'post': post}
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(
            slug=category_slug,
            is_published=True
        )
    )
    post_list = get_list_or_404(
        Post.objects.select_related(
            'category',
            'author',
            'location'
        ).filter(
            category__slug=category_slug,
            is_published=True,
            pub_date__lte=datetime.now()
        )
    )
    context = {
        'post_list': post_list,
        'category': category  
    }
    return render(request, template_name, context)
