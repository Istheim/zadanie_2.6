from django.urls import path
from django.views.decorators.cache import cache_page

from . import views
from catalog.views import contacts, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, \
    CategoryCreateView, CategoryListView, CategoryUpdateView, CategoryDeleteView, CategoryView, \
    ProductModeratorUpdateView

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contacts/', contacts, name='contact'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>', ProductUpdateView.as_view(), name='update_product'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
    path('moderate/<int:pk>/', ProductModeratorUpdateView.as_view(), name='moderate_product'),
    path('create_category/', CategoryCreateView.as_view(), name='create_category'),
    path('category', cache_page(60)(CategoryListView.as_view()), name='category_list'),
    path('category_products/<int:pk>/', cache_page(60)(CategoryView.as_view()), name='category_products'),
    path('category_edit/<int:pk>/', CategoryUpdateView.as_view(), name='edit_category'),
    path('category_delete/<int:pk>/', CategoryDeleteView.as_view(), name='delete_category'),
]