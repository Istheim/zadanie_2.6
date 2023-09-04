from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404
from builtins import *
from pytils.translit import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Product, Version, Category
from catalog.forms import ProductForm, VersionForm


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


# def great_prod(request):
#    """Представление страницы main/great_prod.html с формой загрузки нового прожукта"""
#   product_for_create = []
#   if request.method == 'POST':
#       product_all = {
#           'title': request.POST.get('title'),
#           'description': request.POST.get('description'),
#           'category': request.POST.get('category'),
#           'price': request.POST.get('price'),
#           'first_data': datetime.now(),
#           'last_data': datetime.now()
#       }
#       product_for_create.append(
#           Product(**product_all)
#       )
#       # загрузка нового продукта в БД
#       Product.objects.bulk_create(product_for_create)
#
#    return render(request, 'main/great_prod.html')


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('index')
    template_name = 'main/product_form.html'

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('index')
    template_name = 'main/product_form.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)

        context_data['formset'] = formset

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('index')
    template_name = 'main/product_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser


class VersionListView(ListView):
    model = Version
    template_name = 'main/version.html'


class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('main/version.html')

class CategoryListView(LoginRequiredMixin, ListView):
    """Главная старница со списком товаров"""
    model = Category

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['categories'] = get_cached_categories()
        return context_data


class CategoryView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category = Category.objects.get(pk=self.kwargs['pk'])
        return Product.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['categories'] = get_cached_categories()
        return context_data


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        CategoryFormset = inlineformset_factory(Category, Product, form=CategoryForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = CategoryFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = CategoryFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')

    def test_func(self):
        return self.request.user.is_superuser