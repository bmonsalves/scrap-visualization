import bs4
import requests

from scrapper.config.config import config
from scrapper.config.config import str_slug
from reporting.models import Category


class HomePage:

    def __init__(self, site_uid, enterprise):
        self._config = config()['sites'][site_uid]
        self._selectors = self._config['selectors']
        self._enterprise = enterprise
        self._html = None
        self._go_to_page(self._config['url'])

    @property
    def categories_list(self):
        links = []
        for link in self._select_node(self._selectors['menu_categories']):
            if link and link.has_attr('href'):
                category, created = Category.objects.get_or_create(
                    slug=str_slug(link.text),
                    enterprise_id=self._enterprise.id
                )

                if not category.name:
                    category.name = link.text.strip()

                if not category.url:
                    category.url = link['href']

                category.save()

                pagination = self._selectors['pagination']

                if self._config['url'] in link['href']:
                    new_link = link['href'] + pagination
                else:
                    new_link = (self._config['url'] + link['href'] + pagination)

                links.append({"link": new_link, "category": category})

        return links

    def _go_to_page(self, url):
        response = requests.get(url)
        response.raise_for_status()
        self._html = bs4.BeautifulSoup(response.text, 'html.parser')

    def _select_node(self, selector):
        return self._html.select(selector)
