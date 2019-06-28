from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponse 
from django.contrib.auth.decorators import login_required, user_passes_test 

from products.forms import ProductForm
from products.models import Product, Category, ProductImage
from random import random 



def is_staff(user):
    return user.is_staff
	

def products(request):
    products = Product.objects.all()
    featured_products = Product.objects.filter(featured=True)[0:4]
    
    request.session.setdefault('products_in_cart', [])
    request.session.save()
    
    return render(request,'products.html', context={'products':products,
													'featured_products':featured_products})
@login_required
@user_passes_test(is_staff)											
def create_product(request):
	if request.method == 'GET':
		product_form = ProductForm() 
		return render(request,'create_product.html', context={'product_form':product_form})
        
	elif request.method == 'POST':
		product_form = ProductForm(request.POST)
		if product_form.is_valid():
			product = product_form.save()
			
			images = ['image_1', 'image_2', 'image_3']
			
			for image in images:
				url = product_form.cleaned_data.get(image)
				if url: 
					ProductImage.objects.create(product=product, url=url)
					
			return redirect('/products')

		return render(request, 'create_product.html', context={'product_form':product_form})

@login_required
@user_passes_test(is_staff)
def edit_product(request, product_id):
	product = get_object_or_404(Product, id=product_id)
      
	if request.method == 'GET':
		product_form = ProductForm(instance=product)
		return render(request,'edit_product.html', context={'product_form':product_form,
															'product':product})
    
	elif request.method == 'POST':
		
		
		product_form = ProductForm(request.POST, instance=product)
		if product_form.is_valid():
			product = product_form.save()
			
	
			images = ['image_1', 'image_2', 'image_3']
			
			product_images = product.productimage_set.all()
			old_product_urls = [image.url for image in product_images]
			
			
			new_product_urls = [product_form.cleaned_data.get(image) for image in images
								if product_form.cleaned_data.get(image)]
				
			for url in old_product_urls:
				if url not in new_product_urls:
					product_image = ProductImage.objects.filter(url=url)
					product_image.delete()
					
			
			for url in new_product_urls:
				if url in old_product_urls:
					continue 
				ProductImage.objects.create(product=product,url=url)
				
			return redirect('products')
		
		return render(request,'create_product.html',context={'product_form':product_form,
															'product':product})
	
@login_required
@user_passes_test(is_staff)
def delete_product(request, product_id):
	product = get_object_or_404(Product,id=product_id)
	if request.method == 'GET':
		return render(request,'delete_product.html',context={'product':product})
	elif request.method == "POST":
		product.delete()
		return redirect('products')


@login_required
@user_passes_test(is_staff)
def toggle_featured(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	product.featured = not product.featured
	product.save()
	return redirect('products')


@login_required
def cart(request):
	product_ids = request.session.get('products_in_cart')
	products_in_cart = Product.objects.filter(id__in=product_ids)
	return render(request, 'cart.html', context={'products_in_cart':products_in_cart})
	

@login_required
def add_to_cart(request):
	product_id = request.POST.get('product_id')
	request.session['products_in_cart'].append(product_id)
	request.session.save()
	return redirect('products')
	
@login_required
def remove_from_cart(request):
	product_id = request.POST.get('product_id')
	request.session['products_in_cart'].remove(product_id)
	request.session.save()
	return redirect('cart')
	
	 
