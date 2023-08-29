from django.urls import path
from . import views
from catalog.views import contacts, ProductListView, ProductDetailView

from blogs.apps import BlogsConfig
from .views import BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView

app_name = BlogsConfig.name

urlpatterns = [
    path('create', BlogCreateView.as_view(), name='create'),
    path('', BlogListView.as_view(), name='list'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='edit'),
    path('view/<int:pk>/', BlogDetailView.as_view(), name='view'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
]
