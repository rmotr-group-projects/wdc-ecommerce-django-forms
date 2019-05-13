from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Product, Category, ProductImage


# class ProductForm(forms.Form):
    # name = forms.CharField(label='Name', max_length=200)
    # sku = forms.CharField(label='SKU', max_length=8, min_length=8)
    # category = forms.ModelChoiceField(label='Category', queryset=Category.objects.all())
    # description = forms.CharField(label='Description', max_length=1000, required=False)
    # price = forms.FloatField(label='Price', min_value=0)
    # image_1 = forms.URLField(label='Image 1', required=False)
    # image_2 = forms.URLField(label='Image 2', required=False)
    # image_3 = forms.URLField(label='Image 3', required=False)

    # CODE ABOVE IS JUST AN EXAMPLE OF A REGULAR DJANGO FORM.


class ProductForm(forms.ModelForm):
    image_1 = forms.URLField(required=False)
    image_2 = forms.URLField(required=False)
    image_3 = forms.URLField(required=False)

    class Meta:
        model = Product
        fields = ['name', 'sku', 'category', 'description', 'price']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        product = self.instance
        # Loop through all product images and assign one image URL to each
        # image_1, image_2 and image_3 form fields

        # YOUR CODE HERE
        product_images = [image.url for image in product.productimage_set.all()]

        for i in range(len(product_images)):
            field = self.fields.get('image_{}'.format(i + 1))
            field.initial = product_images[i]
