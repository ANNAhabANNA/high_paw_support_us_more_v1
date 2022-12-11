from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product

# Create your views here.

def review_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_product(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    # Gets quantity from the view.
    quantity = int(request.POST.get('quantity'))

    redirect_url = request.POST.get('redirect_url')

    # Gets product size from the view.
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']

    # Allows us to store the contents of the shopping bag in the HTTP session.
    bag = request.session.get('bag', {})

    # Makes some adjustments to the structure of the bag if a product with sizes is being added.
    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
            else:
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    # Overwrite the variable in the session with the updated version.
    request.session['bag'] = bag
    return redirect(redirect_url)

def adjust_product(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    request.session['bag'] = bag
    return redirect(reverse('review_bag'))

def remove_product(request, item_id):
    """Remove the product from the shopping bag"""

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        else:
            bag.pop(item_id)

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)