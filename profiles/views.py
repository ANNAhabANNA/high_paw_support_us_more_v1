from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm

# User profile views from Boutique Ado
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    # POST handler
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

    # Populates the form with user's current profile information.
    form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/user_profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)

def order_history(request, order_number):
    ''' Displays user order history'''
    # Gets the order.
    order = get_object_or_404(Order, order_number=order_number)

    # Past order confirmation message.
    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/payment_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)