import bs4
import requests
import re

from scrapper.config.config import config


class CategoryList:

    def __init__(self, site_uid, url):
        self._config = config()['sites'][site_uid]
        self._selectors = self._config['selectors']
        self._html = None
        self.go_to_page(url)

    @property
    def products_list(self):
        links = []
        for link in self._select_node(self._selectors['product_link']):
            if link and link.has_attr('href'):
                if self._config['url'] in link['href']:
                    links.append(link['href'])
                else:
                    format_link = (self._config['url'] + link['href'])
                    links.append(format_link)

        return set(links)

    @property
    def total_products(self):
        total = self._select_node(self._selectors['total_products'])
        if total:
            str1 = bs4.BeautifulSoup(repr(self._select_node(self._selectors['total_products'])[0])).text
            return int(re.search(r'\d+', str1).group(0))

    @property
    def total_pages(self):
        total_products = self.total_products
        items_per_page = self._selectors['items_per_page']

        if (total_products is None) or (items_per_page is None):
            return 0

        total_pages = round(total_products / items_per_page)
        return total_pages if total_pages > 0 else 1

    def go_to_page(self, url):
        response = requests.get(url)
        response.raise_for_status()
        self._html = bs4.BeautifulSoup(response.text, 'html.parser')

    def _select_node(self, selector):
        return self._html.select(selector)
