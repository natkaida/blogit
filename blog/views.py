from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Tag, Category
from django.contrib import messages
from django.http import HttpResponseRedirect
from users.models import Profile
from .forms import PostForm, CommentForm
from .utils import searchPosts
from users.utils import paginateObjects

@login_required
def createPost(request):
    profile = request.user.profile
    form = PostForm()

    if request.method == 'POST':
        request.POST.getlist('tags')
        newtags = request.POST.get('newtags').replace(',',  " ").split()
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save()
            post.owner = profile
            post.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                post.tags.add(tag)
            
            return redirect("blog:my-blog")

    context = {'form': form}
    return render(request, "blog/post_form.html", context)

@login_required    
def userBlog(request, username):
    profile = Profile.objects.get(username=username)
    posts = profile.post_set.all()
    tags, categories = get_tags_categories(posts)
    custom_range, posts = paginateObjects(request, posts, 3)
    context = {'profile': profile, 'posts': posts,
                'tags': tags, 'categories': categories,
               'custom_range': custom_range}

    return render(request, "blog/user-blog.html", context)

@login_required
def post(request, post_slug):
    post = Post.objects.get(slug=post_slug)
    profile = request.user.profile
    comments = post.comments.filter(approved=True)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.post = post
        comment.owner = request.user.profile
        comment.save()
        messages.success(request, 'Ваш комментарий появится после проверки модератором')
        return redirect('blog:post', post_slug=post.slug)    
    return render(request, 'blog/single-post.html', 
        {'post': post, 'profile': profile, 
        'comments': comments, 'form': form})

def get_tags_categories(posts):
    categories = set()
    tags = set()
    for post in posts:
        categories.add(post.category)
        for tag in post.tags.all():
            tags.add(tag)
    return tags, categories

@login_required
def myBlog(request):
    profile = request.user.profile
    posts = profile.post_set.all()
    tags, categories = get_tags_categories(posts)
 
    custom_range, posts = paginateObjects(request, posts, 3)
    context = {'profile': profile, 'posts': posts, 
    'custom_range': custom_range, 'tags': tags, 
    'categories': categories}
    return render(request, 'blog/my-blog.html', context)

@login_required
def updatePost(request, pk):
    profile = request.user.profile
    post = profile.post_set.get(id=pk)
    form = PostForm(instance=post)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()

        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                post.tags.add(tag)

            return redirect('blog:my-blog')

    context = {'form': form, 'post': post}
    return render(request, "blog/post_form.html", context)


@login_required
def deletePost(request, pk):
    profile = request.user.profile
    post = profile.post_set.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:my-blog')
    context = {'object': post}
    return render(request, 'delete_template.html', context)

@login_required
def like_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        if not post.likes.filter(id=request.user.id).exists():
            post.likes.add(request.user)
            post.save() 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            post.likes.remove(request.user)
            post.save() 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def bookmark_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        if not post.bookmarks.filter(id=request.user.id).exists():
            post.bookmarks.add(request.user)
            post.save() 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            post.bookmarks.remove(request.user)
            post.save() 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))            

@login_required
def friends(request):
    profile = request.user.profile
    posts = Post.objects.filter(
        owner__in=profile.follows.all()
    )

    tags, categories = get_tags_categories(posts)
    posts, search_query = searchPosts(request)
    custom_range, posts = paginateObjects(request, posts, 3)
    context = {'profile': profile, 'posts': posts, 
    'search_query': search_query, 
    'custom_range': custom_range, 
    'tags': tags, 'categories': categories}
    return render(request, 'blog/post_list.html', context)

@login_required
def user_bookmarks(request):
    profile = request.user.profile
    user = request.user
    posts = Post.objects.filter(bookmarks__in=[user])
    tags, categories = get_tags_categories(posts)
 
    custom_range, posts = paginateObjects(request, posts, 3)
    context = {'profile': profile, "posts": posts, 
    'custom_range': custom_range, 
    'tags': tags, 'categories': categories}

    return render(request, "blog/post_list.html", context)

@login_required
def posts_by_category(request, category_slug):
    profile = request.user.profile
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category__slug__contains = category_slug)  
    tags, categories = get_tags_categories(posts)
 
    custom_range, posts = paginateObjects(request, posts, 3)
    context = {'profile': profile, 'posts': posts, 
    'custom_range': custom_range, 'tags': tags, 
    'category': category, 'categories': categories}
    return render(request, "blog/post_list.html", context)  

@login_required
def posts_by_tag(request, tag_slug):
    profile = request.user.profile
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags__in=[tag])
    tags, categories = get_tags_categories(posts)
 
    custom_range, posts = paginateObjects(request, posts, 3)
    context = {'profile': profile, 'posts': posts, 
    'custom_range': custom_range, 'tags': tags, 
    'tag': tag, 'categories': categories}
    return render(request, "blog/post_list.html", context)     