from django.shortcuts import render
from django.views import generic
from .models import BlogPost
from django.views.generic import ListView


class BlogList(ListView):
    """Creates the post on the blog"""
    model = BlogPost
    template_name = 'blog/blog.html'
