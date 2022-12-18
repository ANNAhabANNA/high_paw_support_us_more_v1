from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required

from .models import Product, Category
from .forms import ProductForm

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    # Sorting functionality based on Boutique Ado project
    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey

            # case-sensitive sorting
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            # descending sorting
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

            if 'category' in request.GET:
                categories = request.GET['category'].split(',')
                products = products.filter(category__name__in=categories)
                categories = Category.objects.filter(name__in=categories)

    # Search bar functionality from Boutique Ado project
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    # Returns the current sorting methodology to the template
    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    """ A view to show individual product details """

    # Product id as a parameter returns just one product
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)

def add_inventory(request):
    """ Adds a new inventory item """
    
    # POST handler
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Store inventory has been updated!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add inventory. Please check the form is valid.')
    else:
        form = ProductForm()
  
    template = 'products/add_inventory.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

def edit_inventory(request, product_id):
    """ Updates an inventory item """

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        # Instantiates a form if request method is POST
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated inventory!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update inventory. Please check the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are updating {product.name}')

    template = 'products/edit_inventory.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

def delete_inventory(request, product_id):
    """ Deletes an inventory item """

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Inventory deleted!')
    return redirect(reverse('products'))

@login_required
def add_to_wishlist(request, product_id):
    ''' A view to add or remove products from user's wishlist'''
    product = get_object_or_404(Product, id=product_id)
    if product.user_wishlist.filter(id=request.user.id).exists():
        product.user_wishlist.remove(request.user)
        messages.success(
            request,
            f'{ product.name } removed from your Wishlist'
        )
        
    else:
        product.user_wishlist.add(request.user)
        messages.success(
            request,
            f'{ product.name } added to your Wishlist'
        )
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
