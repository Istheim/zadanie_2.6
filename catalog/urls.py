from django.urls import path
from . import views
from catalog.views import contacts, great_prod, ProductListView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contacts/', contacts, name='contact'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('great_prod/', great_prod)
]
