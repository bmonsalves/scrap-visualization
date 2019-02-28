from django.http import HttpResponse
from django.shortcuts import render
from reporting.models import Product, Enterprise


def index(request):
    return HttpResponse("reporting")


def products(request, enterprise_id):
    enterprise = Enterprise.objects.get(id=enterprise_id)
    products = Product.objects.filter(enterprise_id=enterprise_id)
    return render(request, 'products_list.html', {'products': products, 'enterprise': enterprise})

def product(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product, 'enterprise': product.enterprise})
