from spellchecker.models import MatchedError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from scrapyd_api import ScrapydAPI

import json


from uuid import uuid4


scrapy_api = ScrapydAPI('http://localhost:6800')


@csrf_exempt # to exempt cross-site request forgery check
@require_POST # to make sure that the request is POST
def checker(request):
    
    # Get the url to check
    url = json.loads(request.body)['url']  

    # Get language
    language = json.loads(request.body).get('language')

    job_id = str(uuid4()) # create a unique ID for this request. 
    
    # Schedule the spider and return the task_id
    task_id = scrapy_api.schedule('default', 'SpellCheckerSpider', url=url, language=language, job_id=job_id)

    # Check the status of the task
    job_status = scrapy_api.job_status('default', task_id)

    # wait until job_status is finished
    while job_status != 'finished':
        job_status = scrapy_api.job_status('default', task_id)

    
    # Task is complete, get the results
    items = MatchedError.serializeable.serialize(job_id)

    return JsonResponse({'results': items, 'size': len(items)})

    

