from datetime import datetime

from django.shortcuts import render, get_object_or_404
from builtins import *
from pytils.translit import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Product
from catalog.forms import ProductForm


class ProductListView(ListView):
    model = Product
    template_name = 'main/index.html'


def contacts(request):
    if request == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name}, {phone}, ({message})')
    return render(request, 'main/contacts.html')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product.html'


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


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('index')

    # def form_valid(self, form):
    #     if form.is_valid():
    #         new_mat = form.save()
    #         new_mat.slug = slugify(new_mat.title_post)
    #         new_mat.save()
    #
    #     return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('index')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('index')
