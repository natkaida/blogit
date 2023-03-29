from .models import Profile, Interest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


def paginateObjects(request, objects, results):
    page = request.GET.get('page')
    paginator = Paginator(objects, results)

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        objects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        objects = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, objects


def searchProfiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    interest = Interest.objects.filter(name__icontains=search_query)
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user).distinct().filter(
        Q(name__icontains=search_query) |
        Q(summary__icontains=search_query) |
        Q(interest__in=interest)
    )
    else:
        profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(summary__icontains=search_query) |
        Q(interest__in=interest)
    )
    return profiles, search_query

