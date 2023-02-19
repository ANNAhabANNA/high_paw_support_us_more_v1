from django.db import models
from products.models import Product
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from profiles.models import UserProfile
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify


STATUS = ((0, "Draft"), (1, "Added"))


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.SET_NULL)
    slug = models.SlugField(max_length=200, unique=True, null=True,)
    title = models.CharField(
        default='Title',
        max_length=100,
        blank=True,
        null=False
    )
    comment = models.TextField(
        default='Leave your comment here',
        max_length=500,
        blank=True,
        null=False
    )
    rating = models.IntegerField(
        default=3,
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        null=False
    )
    status = models.IntegerField(choices=STATUS, default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Review, self).save(*args, **kwargs)
