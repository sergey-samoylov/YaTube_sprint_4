from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404

from .forms import PostForm
from .models import Group, Post, User


POSTS_ON_PAGE = 3


def index(request):
    keyword = request.GET.get("q", None)
    post_list = Post.objects.all().order_by('-pub_date')

    if keyword:
        post_list = post_list.filter(
            text__contains=keyword
            ).select_related('author', 'group').all()

    paginator = Paginator(post_list, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    template = 'posts/index.html'

    context = {
        "page_obj": page_obj,
        "keyword": keyword,
    }
    return render(request, template, context)


@login_required
def group_posts(request, slug):
    keyword = request.GET.get("q", None)
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by('-pub_date')

    if keyword:
        post_list = post_list.filter(
            text__contains=keyword
            ).select_related('author', 'group').all()

    paginator = Paginator(post_list, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    template = 'posts/group_list.html'

    context = {
        'group': group,
        "keyword": keyword,
        "page_obj": page_obj,
    }
    return render(request, template, context)

@login_required
def profile(request, username):
    keyword = request.GET.get("q", None)
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all().order_by('-pub_date')

    if keyword:
        post_list = post_list.filter(
            text__contains=keyword
            ).select_related('author', 'group').all()

    paginator = Paginator(post_list, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    template = 'posts/profile.html'

    context = {
        'author': author,
        'paginator': paginator,
        'page_number': page_number,
        'page_obj': page_obj,
        'post_list': post_list,
    }
    return render(request, template, context)


@login_required
def post_detail(request, post_id):
    keyword = request.GET.get("q", None)
    post = get_object_or_404(Post, pk=post_id)

    if keyword:
        return redirect("posts:index")

    template =  'posts/post_detail.html'

    context = {
        'post': post,
    }

    return render(request, template, context)

def post_create(request):
    username = request.user.username
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("posts:profile", username)
    is_edit = False
    form = PostForm()
    template = 'posts/post_create.html'

    context = {
        'is_edit': is_edit,
        'form': form,
    }

    return render(request, template, context)

def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect("posts:post_detail", post_id)
    form = PostForm(request.POST or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form = form.save(commit=False)
        form.save()
        return redirect("posts:post_detail", post_id)
    is_edit = True
    template = 'posts/post_create.html'

    context = {
        'is_edit': is_edit,
        'form': form,
    }

    return render(request, template, context)
