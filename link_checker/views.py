from link_checker.models import LinkModel
from django.shortcuts import redirect, render
from django.urls import reverse
from scrapyd_api import ScrapydAPI

scrapy_api = ScrapydAPI('http://localhost:6800')


def get_urls(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        task_id = scrapy_api.schedule('default', 'link_spider', url=url)

        return redirect(f"{reverse('results')}?task_id={task_id}")

    return render(request, 'link_checker/get_urls.html')


def results(request):
    task_id = request.GET.get('task_id')
    job_status = scrapy_api.job_status('default', task_id)
    print(f"\n\n\n{job_status}\n\n\n")
    if job_status == 'finished':
        items = LinkModel.objects.all().order_by('-pk')
        return render(request, 'link_checker/results.html', {'items': items})      
    return render(request, 'link_checker/results.html')
