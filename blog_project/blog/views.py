from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    posts = Post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, year, month, day, post):
    # Queries with field lookup methods are built using two underscores.
    # It also could be used for accessing fields of related models.
    # Here we use two underscores to access fields year, month and day of
    # the publish record
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
