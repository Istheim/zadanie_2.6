from datetime import datetime

from django.shortcuts import render, get_object_or_404
from builtins import *

from catalog.models import Product


# Create your views here.


def index(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list
    }
    return render(request, 'main/index.html', context)


def contacts(request):
    if request == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name}, {phone}, ({message})')
    return render(request, 'main/contacts.html')


def product(request, product_id):
    """представление страницы main/product.html для каждого продукта"""
    prod_get = get_object_or_404(Product, pk=product_id)

    return render(request, 'main/product.html', {'product': prod_get})


def great_prod(request):
    """Представление страницы main/great_prod.html с формой загрузки нового прожукта"""
    product_for_create = []
    if request.method == 'POST':
        product_all = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'category': request.POST.get('category'),
            'price': request.POST.get('price'),
            'first_data': datetime.now(),
            'last_data': datetime.now()
        }
        product_for_create.append(
            Product(**product_all)
        )
        # загрузка нового продукта в БД
        Product.objects.bulk_create(product_for_create)

    return render(request, 'main/great_prod.html')
