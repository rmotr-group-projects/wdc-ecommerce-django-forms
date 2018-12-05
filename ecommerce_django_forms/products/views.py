from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound

from products.forms import ProductForm
from products.models import Product, Category, ProductImage


def products(request):
    products = Product.objects.filter(active=True)

    # get up to 4 featured products
    featured_products = Product.objects.filter(featured=True)[:4]

    # initialize list of products in cart for current session
    request.session.setdefault('products_in_cart', [])
    request.session.save()

    return render(
        request,
        'products.html',
        context={'products': products, 'featured_products': featured_products}
    )


def create_product(request):
    if request.method == 'GET':
        # create an instance of ProductFrom and render "create_product.html"
        # sending the form as context under "product_form" key
        product_form = ProductForm()
        return render(
            request,
            'create_product.html',
            context={'product_form': product_form}
        )
    elif request.method == 'POST':
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product = product_form.save()

            # create product images
            images = []
            for i in range(3):
                image = product_form.cleaned_data['image_{}'.format(i + 1)]
                if image:
                    images.append(image)

            for image in images:
                ProductImage.objects.create(
                    product=product,
                    url=image
                )
            return redirect('products')

        return render(
            request,
            'create_product.html',
            context={'product_form': product_form}
        )


def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'GET':
        product_form = ProductForm(instance=product)
        return render(
            request,
            'edit_product.html',
            context={
                'product': product,
                'product_form': product_form
            }
        )
    elif request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        if product_form.is_valid():
            product = product_form.save()

            # Create new images that came in payload, and delete the ones that
            # didn't came in payload but are already created in the DB
            new_images = []
            for i in range(3):
                image = product_form.cleaned_data['image_{}'.format(i + 1)]
                if image:
                    new_images.append(image)

            old_images = [image.url for image in product.productimage_set.all()]

            images_to_delete = []
            for image in old_images:
                if image not in new_images:
                    images_to_delete.append(image)
            ProductImage.objects.filter(url__in=images_to_delete).delete()

            for image in new_images:
                if image not in old_images:
                    ProductImage.objects.create(
                        product=product,
                        url=image
                    )
            return redirect('products')

        return render(
            request,
            'edit_product.html',
            context={
                'product': product,
                'product_form': product_form
            }
        )


def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'GET':
        return render(request, 'delete_product.html', context={'product': product})
    elif request.method == "POST":
        product.delete()
        return redirect('products')


def toggle_featured(request, product_id):
    product = Product.objects.get(id=product_id)
    product.featured = not product.featured
    product.save()
    return redirect('products')


def cart(request):
    products_ids = request.session.get('products_in_cart', [])
    products_in_cart = Product.objects.filter(id__in=products_ids)
    return render(
        request,
        'cart.html',
        context={
            'products_in_cart': products_in_cart,
        }
    )


def add_to_cart(request):
    request.session.setdefault('products_in_cart', [])
    request.session['products_in_cart'].append(request.POST.get('product_id'))
    request.session.save()
    return redirect('products')


def remove_from_cart(request):
    if request.session.get('products_in_cart'):
        request.session['products_in_cart'].remove(request.POST.get('product_id')   )
        request.session.save()
    return redirect('cart')
