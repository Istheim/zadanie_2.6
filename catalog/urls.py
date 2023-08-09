from django.urls import path
from . import views
from catalog.views import contacts, great_prod, product, index

urlpatterns = [
    path('', index),
    path('contacts/', contacts, name='contacts'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('great_prod/', great_prod)
]
