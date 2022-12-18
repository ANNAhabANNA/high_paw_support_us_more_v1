from django import forms
from .models import Review
from django.forms import HiddenInput


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'comment', 'rating']


class ApproveForm(forms.ModelForm):
    """Form to Approve Reviews"""
    class Meta:
        model = Review
        fields = ('slug', 'status',)
        widgets = {'slug': HiddenInput(),}