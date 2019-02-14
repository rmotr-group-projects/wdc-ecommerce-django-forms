from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound

from products.forms import ProductForm
from products.models import Product, Category, ProductImage


def products(request):
    products = Product.objects.all()
    featured_products = Product.objects.filter(featured=True)[:4]
    request.session.setdefault('products_in_cart', [])
    request.session.save()
    return render(request, 'products.html', {'products': products, 'featured_products': featured_products})


def create_product(request):
    product_form = ProductForm(request.POST or None)
    if request.method == 'POST':
        if product_form.is_valid():
            product = product_form.save()
            if product_form.cleaned_data.get('image_1'):
                ProductImage.objects.create(product=product, url=product_form.cleaned_data.get('image_1'))

            if product_form.cleaned_data.get('image_2'):
                ProductImage.objects.create(product=product, url=product_form.cleaned_data.get('image_2'))

            if product_form.cleaned_data.get('image_3'):
                ProductImage.objects.create(product=product, url=product_form.cleaned_data.get('image_3'))
            return redirect('products')
    return render(request, 'create_product.html', {'product_form': product_form})


def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product_form = ProductForm(request.POST or None, instance=product)
    if request.method == 'POST':

        if product_form.is_valid():
            product = product_form.save()
            all_images = product.productimage_set.all().delete()

            if product_form.cleaned_data.get('image_1'):
                ProductImage.objects.create(product=product, url=product_form.cleaned_data.get('image_1'))

            if product_form.cleaned_data.get('image_2'):
                ProductImage.objects.create(product=product, url=product_form.cleaned_data.get('image_2'))

            if product_form.cleaned_data.get('image_3'):
                ProductImage.objects.create(product=product, url=product_form.cleaned_data.get('image_3'))

            return redirect('products')

    return render(request, 'edit_product.html', {'product': product, 'product_form': product_form})


def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        product.delete()
        return redirect('products')
    return render(request, 'delete_product.html', {'product': product})


def toggle_featured(request, product_id):
    product = Product.objects.get(id=product_id)
    product.featured = not product.featured
    product.save()
    return redirect('products')


def cart(request):
    products_ids = request.session['products_in_cart']
    products_in_cart = Product.objects.filter(id__in=products_ids)
    return render(request, 'cart.html', {'products_in_cart': products_in_cart})


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        request.session['products_in_cart'].append(product_id)
        request.session.save()
    return redirect('products')


def remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        request.session['products_in_cart'].remove(product_id)
        request.session.save()
    return redirect('cart')
