from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from products.models import Category, Product, ProductImage
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Imports initial data'

    def handle(self, *args, **options):
        User.objects.all().delete()
        Category.objects.all().delete()
        Product.objects.all().delete()
        ProductImage.objects.all().delete()

        User.objects.create_superuser(
            username='admin', email='admin@example.com', password='admin')
        user = User.objects.create(username='test', email='test@example.com')
        user.set_password('test')
        user.save()

        CATEGORIES = [
            'Shoes', 'Accessories', 'Clothing', 'Sports'
        ]
        categories = []
        for category in CATEGORIES:
            c = Category.objects.create(name=category)
            categories.append(c)

        PRODUCTS = [
            ('Nike Vapor', '44444444', categories[3], 129.99, True),
            ('Nike Cap', '33333333', categories[1], 27.99, True),
            ('Diamond Necklace', '88888888', categories[1], 233, True),
            ('Sweater', '55555555', categories[2], 49.99, True),
            ('Socks', '11111111', categories[2], 8.99, False),
            ('Jean', '22222222', categories[2], 39.99, False),
            ('Rings', '66666666', categories[1], 19.99, False),
            ('Shoes', '77777777', categories[0], 80.99, False),
            ('Leggings', '99999999', categories[3], 29.99, False),
            ('Gloves', '99999999', categories[1], 29.99, False),
        ]
        products = []
        for name, sku, category, price, featured in PRODUCTS:
            p = Product.objects.create(
                name=name,
                sku=sku,
                category=category,
                price=price,
                featured=featured
            )
            products.append(p)

        IMAGES = [
            'https://images-na.ssl-images-amazon.com/images/I/61toIdeEdZL._UX695_.jpg',
            'https://images-na.ssl-images-amazon.com/images/I/61-Rm5tfPML._UX679_.jpg',
            'https://images-na.ssl-images-amazon.com/images/I/61x3zjjiDsL._UY695_.jpg',
            'https://images-na.ssl-images-amazon.com/images/I/51DtYxTRVfL._SX679._SX._UX._SY._UY_.jpg',
            'https://images-na.ssl-images-amazon.com/images/I/61t50Fa1WXL._SL1010_.jpg',
            'https://images-na.ssl-images-amazon.com/images/I/815CjHgZClL._UY879_.jpg',
            'https://images-na.ssl-images-amazon.com/images/I/71DfpJ8EatL._UX679_.jpg',
            'https://images-na.ssl-images-amazon.com/images/I/81gVrGpMBKL._UY695_.jpg',
            'https://images-na.ssl-images-amazon.com/images/I/613I3iAunmL._UX679_.jpg',
            'https://images-na.ssl-images-amazon.com/images/I/71Wu3PZqRLL._UX679_.jpg'
        ]
        for index, image in enumerate(IMAGES):
            ProductImage.objects.create(
                product=products[index],
                url=image
            )
        print('Imported!')
