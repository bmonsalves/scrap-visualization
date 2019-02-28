from django.db import models


class Enterprise(models.Model):
    name = models.TextField(max_length=100, blank=False)
    slug = models.TextField(max_length=100, blank=False)
    url = models.URLField(max_length=300, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    name = models.TextField(max_length=100, blank=False)
    slug = models.TextField(max_length=100, blank=False)
    url = models.URLField(max_length=300, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ManyToManyField(Category)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, blank=False)
    url = models.URLField(blank=False, null=False)
    image = models.URLField(blank=True, null=True)
    sku = models.TextField(max_length=100, blank=True, null=True)
    title = models.TextField(max_length=200, blank=True, null=True)
    subtitle = models.TextField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    internet_price = models.FloatField(blank=True, null=True)
    offer_price = models.FloatField(blank=True, null=True)
    normal_price = models.FloatField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

