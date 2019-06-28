from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Product, Category, ProductImage

class ProductForm(forms.ModelForm):
    CHOICES = [(True, 'Yes'),(False, 'No')]
    image_1 = forms.URLField(required=False)
    image_2 = forms.URLField(required=False)
    image_3 = forms.URLField(required=False)
    featured = forms.ChoiceField(label='Is featured?', choices=CHOICES, initial=CHOICES[0][0])

    class Meta:
        model = Product
        fields = ['name', 'sku', 'category', 'description', 'price', 'featured'] 

    def __init__(self, *args, **kwargs):									
        super(ProductForm, self).__init__(*args, **kwargs)
        product = self.instance
        product_images = [image.url for image in product.productimage_set.all()]
        
        for i in range(len(product_images)):
            field = self.fields.get('image_{}'.format(i+1))
            field.initial = product_images[i]
       
