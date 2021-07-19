from scrapyd_api import ScrapydAPI

scrapy_api = ScrapydAPI('http://localhost:6800')
 
task_id = scrapy_api.schedule('default', 'link_spider', url='http://quotes.toscrape.com/')

job_status = scrapy_api.job_status('default', task_id)
print(job_status)

while job_status != 'finished':
    temp_js = job_status
    job_status = scrapy_api.job_status('default', task_id)

    if temp_js != job_status:
        print(job_status)

print(job_status, task_id)
