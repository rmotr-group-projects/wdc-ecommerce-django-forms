from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound

from products.forms import ProductForm
from products.models import Product, Category, ProductImage


def products(request):
    # Get all products from the DB
    # all_entries = Entry.objects.all()
    #products = Products.objects.all()
    products = Product.objects.filter(active=True) # ACTIVE?!
    
    # Get up to 4 featured products from the DB
    featured_products = Product.objects.filter(featured=True)[:4] #choose first four from list

    # This is done for you. The request.session is a dictionary that contains
    # data that will be stored as long as the user is authenticated.
    # We are just initializing an empty list for the products_in_cart, that will
    # be use later on.
    request.session.setdefault('products_in_cart', [])
    request.session.save()

    # Render 'products.html' template sending products and featured products as context
    # KWARGS!
    return render(request,'products.html',
        context={'products': products, 'featured_products': featured_products}
    )

## QUESTION: REALLY COULD USE A GOOD EXPLANATION OF THESE TWO
def create_product(request):
    if request.method == 'GET':
        # Create an empty instance of ProductFrom() and render "create_product.html"
        # sending the form as context under "product_form" key
        product_form = ProductForm()
        
        return render(request,'create_product.html',
            context={'product_form': product_form}
        )
    
    elif request.method == 'POST':
        # Create an instance of ProductFrom initializing it with the product
        # data that come in request.POST
        product_form = ProductForm(request.POST)
        
        if product_form.is_valid():
            # Create the product object while saving the form
            product = product_form.save()
            ## what happens to the data if you don't save the form?
            ## how long does it persist?

            # Inside product_form.cleaned_data you will find the already
            # validated data for the product. Use the images urls there to
            # create a ProductImage object for each one.

            # YOUR CODE HERE
            images = []
            
            ### CLEANED DATA????????
            ### You fetch the cleaned_data from the ProductForm class
            ### https://stackoverflow.com/questions/52208993/type-object-productform-has-no-attribute-cleaned-data-django
            ### Each field in a Form class is responsible not only for validating data, but also for “cleaning” it – normalizing it to a consistent format.
            ### This is a nice feature, because it allows data for a particular field to be input in a variety of ways, always resulting in consistent output.
            ### What happens if you don't do this?
        
            for i in range(3):
                image = product_form.cleaned_data['image_{}'.format(i + 1)]
                if image:
                    images.append(image)

            for image in images:
                ProductImage.objects.create(product=product,url=image)

            # Redirect to products view
            return redirect('products')

        # If form is not valid, re-render the 'create_product.html' sending the
        # product_form as context, which will have all the error messages included
        return render(request,'create_product.html',context={'product_form': product_form})


def edit_product(request, product_id):
    # Get the product with given product_id from the DB
    product = Product.objects.get(id=product_id)
    
    if request.method == 'GET':
        # Create an instance of ProductForm sending the product in the "instance"
        # parameter. This will initialize all the fields in the form with the
        # data from our product.
        product_form = ProductForm(instance=product) # SEND PRODUCT

        # Render the 'edit_product.html' template sending the product and the
        # product_form as context
        return render(request,'edit_product.html',
            context={
                'product': product,
                'product_form': product_form
            }
        )
    
    elif request.method == 'POST':
        # Create an instance of ProductForm sending the new data that come in
        # request.POST, and also the product inside the "instance" parameter
        product_form = ProductForm(request.POST, instance=product) # INSTANCE is PRODUCT
        
        if product_form.is_valid():
            # Create the product object while saving the form
            ### HOW IS THIS DIFFERENT FROM HOW WE SAVE BEFORE?
            product = product_form.save()

            # Inside product_form.cleaned_data you will find the already
            # validated data for the product. Use the images urls there to
            # create a ProductImage object that are not already created in the DB.
            new_images = []
            for i in range(3):
                image = product_form.cleaned_data['image_{}'.format(i + 1)]
                if image:
                    new_images.append(image)
            
            # The ones that didn't come in cleaned_data and are stored in the DB
            # should be deleted.
            
            # LOAD OLD IMAGES
            # YOUR CODE HERE
            old_images = [image.url for image in product.productimage_set.all()]

            images_to_delete = []
            for image in old_images:
                if image not in new_images:
                    images_to_delete.append(image)
            
###### LOOK THIS UP
            ProductImage.objects.filter(url__in=images_to_delete).delete()
            
            ### CREATE THE PRODUCT IMAGE OBJECT ###
            for image in new_images:
                if image not in old_images:
                    ProductImage.objects.create(product=product,url=image)
            
            # Redirect to 'products' view
            return redirect('products')

        # If form is not valid, re-render the 'create_product.html' sending the
        # product and the product_form as context
        return render(request,'edit_product.html',
            context={
                'product': product,
                'product_form': product_form
            }
        )


def delete_product(request, product_id):
    # Get the product with given product_id from the DB
    product = Product.objects.get(id=product_id)
    
    if request.method == 'GET':
        # Render the 'delete_product.html' template sending the product as context
        return render(request, 'delete_product.html', context={'product': product})
    
    elif request.method == "POST":
        # Delete the product and redirect to 'products' view
        # YOUR CODE HERE
        product.delete()
        return redirect('products')
    

def toggle_featured(request, product_id):
    # Get the product with given product_id from the DB
    product = Product.objects.get(id=product_id)

    # Toggle the boolean product.featured and save the product
    # YOUR CODE HERE
    product.featured = not product.featured
    product.save()
    
    # Redirect to 'products' view
    return redirect('products')


def cart(request):
    # Get all the products ids from the products that have been added to the cart.
    # You can find this ids in the request.session dictionary, under the
    # 'products_in_cart' key. This was explained and initialized in the 'products' view
    products_ids = request.session.get('products_in_cart', [])

    # Get all the products from the DB with the ids above
    products_in_cart = Product.objects.filter(id__in=products_ids)

    # Render the 'cart.html' template sending the products_in_cart as context
    return render(request,'cart.html', context={'products_in_cart': products_in_cart,} )

########################## REVIEW THIS
def add_to_cart(request):
    # Get the product_id that come in request.POST and add it to the
    # list under 'products_in_cart' key of request.session dictionary.
    # Do a .save() to the request.session. This is the way that Django recognizes
    # that something changes in the session.

    # YOUR CODE HERE
    # HOW IS THIS GETTING THE PRODUCT ID
    request.session.setdefault('products_in_cart', [])
    # ADD TO LIST UNDER 'products_in_cart'
    request.session['products_in_cart'].append(request.POST.get('product_id'))
    request.session.save()

    # Redirect to 'products' view
    return redirect('products')


def remove_from_cart(request):
    # Get the product_id that come in request.POST and remove it from the list
    if request.session.get('products_in_cart'):
        
        # under 'products_in_cart' of request.session dictionary.
        request.session['products_in_cart'].remove( request.POST.get('product_id') )
    
        # Do a .save() to the request.session.
        request.session.save()
    
    # YOUR CODE HERE

    # Redirect to 'cart' view
    return redirect('cart')