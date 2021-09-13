from link_scraper.items import MatchedErrorItem
import scrapy
from bs4 import BeautifulSoup as BS
from language_tool_python import LanguageTool as LT
from scrapy.http.response.text import TextResponse


class SpellCheckerSpider(scrapy.Spider):
    name = 'SpellCheckerSpider'
    
    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.language = kwargs.get('language', "en-us")
        self.job_id = kwargs.get('job_id')
        self.language_tool = LT(self.language)
    

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)
        

    def parse(self, response: TextResponse):
        
        lines = response.text.split('\n')
        for line_number, line in enumerate(lines):
            text = BS(line).get_text() 
            matches = self.language_tool.check(text)

            for match in matches:
                # print(f"\n\n\n\n{match}\n\n\n\n")
                yield MatchedErrorItem(
                    message = match.message,
                    error_sentence = match.sentence,
                    error_term = match.matchedText,
                    error_line_number = line_number + 1,
                    page_url = self.url,
                    possibleCorrections = ",".join(match.replacements[:5]),
                    job_id = self.job_id,
                )            

