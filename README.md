<img align="right" width="120" alt="rmotr.com" src="https://user-images.githubusercontent.com/7065401/45454218-80bee800-b6b9-11e8-97bb-bb5e7675f440.png">

# Ecommerce Django Forms

### Setup Instruction

The structure of the whole Django project is built for you. Run the following commands in order to have your local environment up and running.  

```bash
$ mkvirtualenv -p $(which python3) ecommerce_django_forms
$ pip install -r requirements.txt
```

You can now run the development server and point the browser to the correct URL:

```bash
$ make runserver
```

You will have a superuser already created (username: `admin`, password: `admin`) that you can use when pointing to `http://localhost:8080/admin` in your browser with the server running. There you can find the Django admin site where you will be able to create, delete and modify objects from your database.

Also there's a not-admin user (username: `test`, password: `test`) that will be useful for trying the restricted features that this kind of users have while using the Ecommerce platform.

The database already contains some objects that we have created for you, but feel free to interact with it the way you want.

There's also a LIVE version of the solution so you can try it and check how everything should work:

https://ecommerce-django-forms.herokuapp.com/products/

![image](https://user-images.githubusercontent.com/2788551/49392025-01ffa700-f70c-11e8-9a09-a8c5ed7e99b0.png)


### Description

In the [previous part](https://github.com/rmotr-group-projects/wdc-django-html-forms) of Django Ecommerce project, we've developed a solution based on simple HTML forms with manual validation inside the view for each input.

The idea of this advanced version of the project is to migrate all those HTML forms into [Django ModelForms](https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/) that will simplify a lot the validation and rendering of the templates.

Also we'll add a [Session Authentication](https://docs.djangoproject.com/en/2.1/topics/http/sessions/) layer to distinguish different features based on authenticated or not authenticated users, and admin or regular users.

- `Admin` users have access to everything. They can create/edit/delete products, mark products as featured and add products to the shopping cart.
- `Regular` users can only add products to their cart.
- `Anonymous` users (not authenticated) can just view the static products page.

Try all this features with the users credentials and LIVE demo link given above, to make sure how your solution should look like. You can check the code related to the LIVE demo in a branch called `solution` in this same repository.


### Your tasks

#### Task 1: Django forms

For this task you'll have to implement a Django ModelForm related to the Product model. It'll be inside `products/forms.py`. This form will be used later in `create_product` and `edit_product` views and templates.


#### Task 2: Templates and views

We've done the login/logout workflow for you as an example. It is just a new `/accounts` URL that you can check inside `ecommerce_django_forms/urls.py` and a `login.html` template under `templates/registration/login.html`.

Your tasks will be focused on showing/hiding the following buttons in the products page, depending on if user is authenticated or not, and if it has admin permissions or not. Also you'll have to implement the proper view for each button inside `products/views.py`. More explanatory instructions will be written inside views as comments.

- **Shopping cart button**: this button will be available for any authenticated user (admin or not). Views related to this button are `add_to_cart` and `remove_from_cart`.

- **Create|Edit|Delete buttons**: only admin users can see and use this buttons. Views related are `create_product`, `edit_product` and `delete_product`.

- **Featured star**: one more time, admin users are the only ones allowed to toggle a product as featured. The whole featured column in products table should be hide for any other kind of user. Related view is `toggle_featured`.


Make sure to render de ProductForm inside `create_product.html` and `edit_product.html` templates. (HINT: It should be just one single line of code)
