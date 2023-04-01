from django.contrib import admin
from .models import BlogPost, Comment


@admin.register(BlogPost)
class PostAdmin(admin.ModelAdmin):

    list_display = ('tag', 'slug', 'status', 'created_on')
    search_fields = ['tag', 'text']
    list_filter = ('status', 'created_on')
    prepopulated_fields = {'slug': ('tag',)}
    post_fields = ('text',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'generated_on', 'approved')
    list_filter = ('approved', 'generated_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
