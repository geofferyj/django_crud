import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy_djangoitem import DjangoItem
from link_checker.models import LinkModel


class LinkScraperItem(DjangoItem):
    django_model = LinkModel
    
