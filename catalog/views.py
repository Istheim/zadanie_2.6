from datetime import datetime
from builtins import *

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404
from datetime import datetime

from django.views import View
from pytils.translit import slugify
from django.urls import reverse_lazy

from catalog.forms import ProductForm, VersionForm, CategoryForm
from catalog.models import Product, Version, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.services import get_cached_subjects_from_product, get_cached_categories


# Create your views here.
class IndexView(View):
    template_name = 'catalog/index.html'

    def get(self, request):
        products = Product.objects.all()
        return render(request, self.template_name, {'products': products})


class ProductListView(ListView):
    model = Product
    template_name = 'main/index.html'


def contacts(request):
    """Контроллер, который отвечает за отображение контактной информации."""

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(name, phone, message)

    return render(request, 'main/contacts.html')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['product'] = get_cached_subjects_from_product(self.object.pk)
        return context_data


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('index')
    template_name = 'main/product_form.html'


    def form_valid(self, form):
        self.object = form.save()
        self.object.user_boss = self.request.user
        self.object.save()

        # def form_valid(self, form):
        #     if form.is_valid():
        #         new_mat = form.save()
        #         new_mat.slug = slugify(new_mat.title_post)
        #         new_mat.save()

        return super().form_valid(form)


class ProductUpdateView(UpdateView):
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


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('index')
    template_name = 'main/product_confirm_delete.html'


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
