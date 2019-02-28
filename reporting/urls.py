from django.urls import path

from . import views

urlpatterns = [
    path('<int:enterprise_id>/products', views.products, name='products'),
    path('product/<int:product_id>', views.product, name='product')
]
