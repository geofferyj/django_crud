import scrapy


class SpellCheckerSpider(scrapy.Spider):
    name = 'SpellCheckerSpider'
    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
    

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)
        

    def parse(self):
        pass
