from .models import Comment
from django import forms


class CommentBlogForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
