from django.shortcuts import render, redirect

# Create your views here.

def review_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_product(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

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

    # Overwrite the variable in the session with the updated version.
    request.session['bag'] = bag
    return redirect(redirect_url)