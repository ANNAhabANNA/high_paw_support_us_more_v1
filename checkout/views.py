from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from bag.contexts import bag_contents

import stripe
import json

@require_POST
# Checks if the user had the save info box checked.
def cache_checkout_data(request):
    try:
        # Gives client secret from the payment intent.
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Handling of the POST method
    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        # Instance of the form using form_data
        order_form = OrderForm(form_data)
        # If the form is valid the order is saved
        if order_form.is_valid():
            order = order_form.save()
            # Iterates through the bag items to create each line item
            for item_id, item_data in bag.items():
                try:
                    # Gets product id out of shopping bag
                    product = Product.objects.get(id=item_id)
                    # If interger then item has no sizes and quantity will be only item_data
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        # Iteration through items with sizes and creation item line accordingly
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                # If product is not found  adds error message notification
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('review_bag'))

            # User option to save their profile information to the session
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('payment_success', args=[order.order_number]))
        else:
            # If order form is not valid
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))
        
        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)

        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # Instance of order form
        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')
    
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)

def payment_success(request, order_number):
    """
    Takes in order number and renders success payment page
    """

    # Uses the order number to get the order created in checkout view
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    # Success message to notify user of their order number
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    # Deletes the shopping bag from the session
    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/payment_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)