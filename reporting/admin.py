from django.contrib import admin

from .models import Enterprise, Category, Product

admin.site.register(Enterprise)
admin.site.register(Category)
admin.site.register(Product)
