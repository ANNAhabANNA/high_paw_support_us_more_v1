from django import forms
from .models import Review
from django.forms import HiddenInput



class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        exclude = ('product', 'user', 'date_added')


class ApproveForm(forms.ModelForm):
    """Form to Approve Reviews"""
    class Meta:
        model = Review
        fields = ('slug', 'status',)
        widgets = {'slug': HiddenInput(),}