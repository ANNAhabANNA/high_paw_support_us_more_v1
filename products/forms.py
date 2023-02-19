from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


# Extends builtin forms.ModelForm.
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ['user_wishlist']

    # Utilizes CustomClearableFileInput widget
    image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Shows categories with their friendly names.
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        # Updates the category field in the form.
        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
