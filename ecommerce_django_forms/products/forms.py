from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Product, Category, ProductImage




class ProductForm(forms.ModelForm):
    image_1 = forms.URLField(required=False)
    image_2 = forms.URLField(required=False)
    image_3 = forms.URLField(required=False)

    class Meta:
        #Complete model and fields
        model = Product
        fields = ['name', 'sku','category','description','price','active','featured']
        

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        product = self.instance
        #Loop through all product images and assign one image URL to each
        # image_1, image_2 and image_3 form fields
        urls = [pic.url for pic in product.productimage_set.all()]
        for i in range(len(urls)):
            update_field = self.fields.get('image_{}'.format(i+1))
            update_field.inital = urls[i]
            
        
