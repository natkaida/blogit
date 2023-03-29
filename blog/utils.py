from .models import Post, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchPosts(request):
    profile = request.user.profile
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)
    
    posts = Post.objects.filter(
        owner__in=profile.follows.all()
    )
    posts = posts.distinct().filter(
        Q(title__icontains=search_query) |
        Q(text__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )
    return posts, search_query
