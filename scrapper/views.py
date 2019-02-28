from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from reporting.models import Enterprise
from scrapper.config.config import config
from scrapper.config.config import str_slug

import scrapper.page_objects.home_page_object as home
import scrapper.page_objects.category_list_object as category
import scrapper.page_objects.product_page_object as product


def enterprises(request):
    enterprises = Enterprise.objects.all()
    return render(request, 'enterprises.html', {'enterprises': enterprises})


@csrf_exempt
def start_scrap(request):
    if request.method == 'GET':
        site_uid = request.GET.get('page', None)
        if site_uid:
            __config = config()['sites'][site_uid]
            __selectors = __config['selectors']
            logger.info("beggining scraper for {}".format(__config['url']))

            enterprise, created = Enterprise.objects.get_or_create(
                slug=str_slug(site_uid)
            )

            if not enterprise.name:
                enterprise.name = site_uid

            if not enterprise.url:
                enterprise.url = __config['url']

            enterprise.save()

            home_page = home.HomePage(site_uid, enterprise)

            for cat in home_page.categories_list:
                page_number = __selectors['init_page']
                category_list = category.CategoryList(site_uid, cat["link"].replace("PAGE_NUMBER", str(page_number)))
                total_pages = category_list.total_pages

                for i in range(total_pages):
                    url = cat["link"].replace("PAGE_NUMBER", str(page_number))
                    page_number = page_number + __selectors['iterator_page']
                    category_list.go_to_page(url)

                    for item in category_list.products_list:
                        product_item = product.ProductPage(site_uid, item, cat["category"])
                        print(product_item.product)

    enterprises = Enterprise.objects.all()
    return render(request, 'enterprises.html', {'enterprises': enterprises})