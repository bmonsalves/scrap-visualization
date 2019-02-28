import bs4
import requests
import re
from scrapper.config.config import config
from scrapper.config.config import str_slug

from reporting.models import Product


class ProductPage:

    def __init__(self, site_uid, url, category):
        self._config = config()['sites'][site_uid]
        self._selectors = self._config['selectors']['product']
        self._category = category
        self._html = None
        self._url = url
        self._go_to_page(url)

    @property
    def product(self):

        print(self._category)
        product, created = Product.objects.get_or_create(
            sku=self._get_sku(),
            enterprise_id=self._category.enterprise_id
        )

        product.category.add(self._category)
        product.url = self._url
        product.image = self._get_image()
        product.title = self._get_title()
        product.subtitle = self._get_subtitle()
        product.description = self._get_description()
        product.internet_price = self._get_internet_price()
        product.offer_price = self._get_offer_price()
        product.normal_price = self._get_normal_price()
        product.discount = self._get_discount()

        product.save()

        return product

    def _go_to_page(self, url):
        response = requests.get(url)
        response.raise_for_status()
        self._html = bs4.BeautifulSoup(response.text, 'html.parser')

    def _select_node(self, selector):
        return self._html.select(selector)

    def _get_image(self):
        image = self._select_node(self._selectors['image'])
        if image and image[0].has_attr('href'):
            return image[0]['href'].strip()

    def _get_sku(self):
        sku = self._select_node(self._selectors['sku'])
        if sku:
            return sku[0].text.strip().replace(' ', '')

    def _get_title(self):
        title = self._select_node(self._selectors['title'])
        if title:
            return title[0].text.strip()

    def _get_subtitle(self):
        subtitle = self._select_node(self._selectors['subtitle'])
        if subtitle:
            return subtitle[0].text.strip()

    def _get_description(self):
        description = self._select_node(self._selectors['description'])
        if description:
            return description[0].text

    def _get_internet_price(self):
        internet_price = self._select_node(self._selectors['internet_price'])
        if internet_price:
            price = str_slug(internet_price[0].text)
            return int(re.search(r'\d+', price).group())

    def _get_offer_price(self):
        offer_price = self._select_node(self._selectors['offer_price'])
        if offer_price:
            price = str_slug(offer_price[0].text)
            return int(re.search(r'\d+', price).group())

    def _get_normal_price(self):
        normal_price = self._select_node(self._selectors['normal_price'])
        if normal_price:
            price = str_slug(normal_price[0].text)
            return int(re.search(r'\d+', price).group())

    def _get_discount(self):
        discount = self._select_node(self._selectors['discount'])
        if discount:
            price = str_slug(discount[0].text)
            return int(re.search(r'\d+', price).group())
