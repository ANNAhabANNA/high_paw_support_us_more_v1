from django import forms
from .models import Order

# Order form from Boutique Ado project
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # Fields to render.
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        # Sets the form up as it would be by default.
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }

        # Starts the cursor in the full name field when the user loads the page.
        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            # Iterates through the forms fields adding a star to the placeholder if it's a required field on the model.
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                # Sets all the placeholder attributes to their values in the dictionary above.
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # Adds css class.
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # Removes the form fields labels.
            self.fields[field].label = False