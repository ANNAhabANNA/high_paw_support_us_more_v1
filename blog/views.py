from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from .models import BlogPost
from django.views.generic import ListView
from .forms import CommentBlogForm
from django.http import HttpResponseRedirect


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
                "commented": False,
                "liked": liked,
                'comment_form': CommentBlogForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):

        blogpost_collection = BlogPost.objects.filter(status=1)
        post = get_object_or_404(blogpost_collection, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-generated_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentBlogForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentBlogForm()

        return render(
            request,
            "blog/post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )

class PostLike(View):
    """Creates the post like/unlike functionality"""
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(BlogPost, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
