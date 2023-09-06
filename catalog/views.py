from datetime import datetime
from builtins import *
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404
from datetime import datetime

from django.views import View
from pytils.translit import slugify
from django.urls import reverse_lazy

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


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


# def great_prod(request):
#     """Представление страницы main/great_prod.html с формой загрузки нового прожукта"""
#     product_for_create = []
#     if request.method == 'POST':
#         product = {
#             'name_prod': request.POST.get('name'),
#             'description_prod': request.POST.get('description'),
#             'category_prod': request.POST.get('category'),
#             'price_prod': request.POST.get('price'),
#             'data_create_prod': datetime.now(),
#             'data_change_prod': datetime.now(),
#         }
#         product_for_create.append(
#             Product(**product)
#         )
#         # загрузка нового продукта в БД
#         Product.objects.bulk_create(product_for_create)
#
#     return render(request, 'main/great_prod.html')


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
