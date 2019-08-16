from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required, user_passes_test

from products.forms import ProductForm
from products.models import Product, Category, ProductImage

def is_staff(user):
    return user.is_staff
def products(request):
    # Get all products from the DB
    products = Product.objects.all()

    # Get up to 4 featured products from the DB
    featured_products = Product.objects.filter(featured=True)

    # This is done for you. The request.session is a dictionary that contains
    # data that will be stored as long as the user is authenticated.
    # We are just initializing an empty list for the products_in_cart, that will
    # be use later on.
    request.session.setdefault('products_in_cart', [])
    request.session.save()

    # Render 'products.html' template sending products and featured products
    # as context
    return render(request, 'products.html', {'products':products, 'featured_products':featured_products})

@login_required
@user_passes_test(is_staff)
def create_product(request):
    if request.method == 'GET':
        # Create an empty instance of ProductFrom() and render "create_product.html"
        # sending the form as context under "product_form" key
        product_form = ProductForm()
        return render(request, 'create_product.html', {'product_form':product_form})

    elif request.method == 'POST':
        # Create an instance of ProductFrom initializing it with the product
        # data that come in request.POST
                                # bring in entered data
        product_form = ProductForm(request.POST)
        # to make sure data is valid with the field types
        if product_form.is_valid():

            # Create the product object while saving the form
            product = product_form.save()

            # Inside product_form.cleaned_data you will find the already
            # validated data for the product. Use the images urls there to
            # create a ProductImage object for each one.

            # YOUR CODE HERE
            for i in range(3):
                ProductImage.objects.create(
                    product=product, 
                    url=product_form.cleaned_data['image_{}'.format(1+i)])




            # Redirect to products view
            return redirect('products')

        # If form is not valid, re-render the 'create_product.html' sending the
        # product_form as context, which will have all the error messages included
        return render(request,'create_product.html', {'product_form':product_form})

#########################################################################
@login_required
@user_passes_test(is_staff)
def edit_product(request, product_id):


    # Get the product with given product_id from the DB
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'GET':
        # Create an instance of ProductForm sending the product in the "instance"
        # parameter. This will initialize all the fields in the form with the
        # data from our product.
        product_form = ProductForm(instance=product)

        # Render the 'edit_product.html' template sending the product and the
        # product_form as context
        return render(request, 'edit_product.html', {'product':product, 'product_form':product_form})
    elif request.method == 'POST':
        # Create an instance of ProductForm sending the new data that come in
        # request.POST, and also the product inside the "instance" parameter
        product_form = ProductForm(request.POST, instance=product)
        if product_form.is_valid():
            # Create the product object while saving the form
            product = product_form.save()

            # Inside product_form.cleaned_data you will find the already
            # validated data for the product. Use the images urls there to
            # create a ProductImage object that are not already created in the DB.
            # The ones that didn't come in cleaned_data and are stored in the DB
            # should be deleted.

            # YOUR CODE HERE
            to_delete = ProductImage.objects.filter(product=product)
            to_delete.delete()
            for i in range(3):
                ProductImage.objects.create(
                    product=product, 
                    url=product_form.cleaned_data['image_{}'.format(1+i)])

            # Redirect to 'products' view
            return redirect('products')

        # If form is not valid, re-render the 'create_product.html' sending the
        # product and the product_form as context
        return render(request, 'create_product.html', {'product':product, 'product_form':product_form})
####################################################################################
@login_required
@user_passes_test(is_staff)
def delete_product(request, product_id):
    # Get the product with given product_id from the DB
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'GET':
        # Render the 'delete_product.html' template sending the product as context

        
        return render(request, 'delete_product.html', {'product':product})

    elif request.method == "POST":
        # Delete the product and redirect to 'products' view
        # YOUR CODE HERE
        product.delete()

        return redirect('products')

@login_required
@user_passes_test(is_staff)
def toggle_featured(request, product_id):
    # Get the product with given product_id from the DB
    product = get_object_or_404(Product, id=product_id)

    # Toggle the boolean product.featured and save the product
    # YOUR CODE HERE
    if product.featured:
        product.featured = False
    else:
        product.featured = True
    product.save()


    # Redirect to 'products' view
    return redirect('products')

@login_required
def cart(request):
    # Get all the products ids from the products that have been added to the cart.
    # You can find this ids in the request.session dictionary, under the
    # 'products_in_cart' key. This was explained and initialized in the 'products' view
    products_ids = request.session['products_in_cart']

    # Get all the products from the DB with the ids above
    products_in_cart = [Product.objects.get(id=p_id) for p_id in products_ids]

    # Render the 'cart.html' template sending the products_in_cart as context

    return render(request, 'cart.html', {'products_in_cart':products_in_cart})

@login_required
def add_to_cart(request):
    # Get the product_id that come in request.POST and add it to the
    # list under 'products_in_cart' key of request.session dictionary.
    # Do a .save() to the request.session. This is the way that Django recognizes
    # that something changes in the session.

    # YOUR CODE HERE 
    request.session.setdefault('products_in_cart', [])
    request.session['products_in_cart'].append(request.POST.get('product_id'))
    request.session.save()

    # Redirect to 'products' view
    return redirect('products')

@login_required
def remove_from_cart(request):
    # Get the product_id that come in request.POST and remove it from the list
    # under 'products_in_cart' of request.session dictionary.
    # Do a .save() to the request.session.

    # YOUR CODE HERE
    id = request.POST.get('product_id')
    request.session['products_in_cart'].remove(id)
    request.session.save()
    

    # Redirect to 'cart' view
    return redirect('cart')
