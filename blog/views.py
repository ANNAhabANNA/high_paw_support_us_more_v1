from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import BlogPost
from django.views.generic import ListView


class BlogList(ListView):
    """Creates the post on the blog"""
    model = BlogPost
    blogpost_collection = BlogPost.objects.filter(status=1).order_by("-created_on")
    template_name = 'blog/blog.html'


class PostDetail(View):
    """Renders the detailed view of each post including comments"""
    def get(self, request, slug, *args, **kwargs):
        blogpost_collection = BlogPost.objects.filter(status=1)
        post = get_object_or_404(blogpost_collection, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-generated_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "blog/post_detail.html",
            {
                "post": post,
                "comments": comments,
                "liked": liked
            },
        )
