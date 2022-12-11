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

    # Allows us to store the contents of the shopping bag in the HTTP session.
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    # Overwrite the variable in the session with the updated version.
    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)