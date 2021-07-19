from link_scraper.items import LinkScraperItem
from parsel.selector import SelectorList
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst



class LinkSpiderSpider(scrapy.Spider):
    name = 'link_spider'
    # allowed_domains = ['http://quotes.toscrape.com']
    # start_urls = ['http://quotes.toscrape.com/']

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
    

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)
        

    def parse(self, response: TextResponse):
        link_tags: SelectorList = response.css('a')
        
        for link_tag in link_tags:
            loader = ItemLoader(item=LinkScraperItem(), selector=link_tag)
            loader.default_output_processor = TakeFirst()
            loader.add_css('text', 'a::text')
            loader.add_css('url', 'a::attr(href)', TakeFirst(), response.urljoin)
            
            
            yield loader.load_item()
