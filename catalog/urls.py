from django.urls import path
from . import views
from catalog.views import contacts, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, VersionListView, VersionCreateView

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contacts/', contacts, name='contact'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    #path('great_prod/', great_prod),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>', ProductUpdateView.as_view(), name='update_product'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
]
