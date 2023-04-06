from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

STATUS = ((0, "Draft"), (1, "Published"))


class BlogPost(models.Model):
    '''
    Creates an object of a post
    '''
    tag = models.CharField(max_length=210, unique=True)
    slug = models.SlugField(max_length=210, unique=True)
    creator = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="blog_posts"
    )
    image = models.ImageField(null=True, blank=True)
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, 
        related_name='blogpost_like', 
        blank=True
    )

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.tag

    def total_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    '''
    Creates an object of a comment

    '''
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE,
                             related_name="comments")
    name = models.CharField(max_length=75)
    email = models.EmailField()
    body = models.TextField()
    generated_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-generated_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
