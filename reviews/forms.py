from django import forms
from .models import Review
from django.forms import HiddenInput



class ReviewForm(forms.ModelForm):
    """Form to Add Commnents"""
    class Meta:
        model = Review
        exclude = ('product', 'user', 'date_added', 'slug', 'rating', 'status',)
