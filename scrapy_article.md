
## Introduction
Web scraping is the process of harvesting, mining, or extracting data from a web page using some software, this software makes requests to the website as a human would, then parses' (reads) the response based on rules specified by the developer.

The data extracted can be saved into a file, or put into a database.

They are several tools for web scraping, but in this article, we shall be exploring the scrapy library and its integration with Django. 

### Assumptions
I am assuming the following:
1. you know the basics of python development
2. you have or can get python installed on your machine and 
3. you know how to install python libraries using pip.

With that out of the way, let's get building.

Before we get into integrating scrapy with Django, let us first get a feel of the scrapy library.

#### Installing Scrapy
We begin by installing scrapy with the following command.

```console
$ pip install scrapy 
```
#### The Scrapy Shell
Scrapy comes with a shell from where we can test and debug our code. Before creating spiders (more on this later), we will be using the shell to explore some of the capabilities of Scrapy.

Fire up the shell with;
```console
$ scrapy shell
``` 
on the shell, we scrape a webpage with the `fetch()` method;
```repl
>>> fetch("http://quotes.toscrape.com")
```
this will print out the following

```plaintext
2021-07-15 01:21:37 [scrapy.core.engine] INFO: Spider opened
2021-07-15 01:21:38 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://quotes.toscrape.com> (referer: None)
```
The `fetch()` method returns a `HTTPResponse` stored in a variable called `response`. From this variable, we can access the contents of the webpage, the status of the request, etc.

to check the HTTP status of our request, do the following:
```repl
>>> response.status
200
```

#### Extracting data from the response
We can easily get various elements and their contents using `scrapy Selectors`. Scrapy provides 2 main Selectors, the `CSS selector` and the `xpath selector` but we'll be working solely with the CSS selector.

Scrapy's `css selector` takes CSS selectors as arguments and returns all available matches on the page, for example, say we wanted to get all links on a page, we would do the following.

```repl
>>> response.css('a')
```

This would return a list of `Selector` objects, adding a `.get()` 
```repl
>>> response.css('a').get()
```

will return the first `a` tag on the page,
```plaintext
<a href="/" style="text-decoration: none">Quotes to Scrape</a>
```
while adding a `.getall()` ,
```repl
>>> response.css('a').getall()
```
will return all `a` tags on the page.

### Creating a Scrapy Project
Now that we've explored the library from the shell, we shall continue by creating a scrapy project.

We create a scrapy project using the `startproject` command with the name of the project as an argument like so:

```console
scrapy startproject link_scraper
```
we should see the following output in the terminal:

```plaintext
New Scrapy project 'link_scraper', using template directory '~/python3.8/site-packages/scrapy/templates/project', created in:
~/link_scraper

You can start your first spider with:
    cd link_scraper
    scrapy genspider example example.com
```
The command will produce the following directory structure:

```plaintext
.
└── link_scraper
    ├── link_scraper
    │   ├── __init__.py
    │   ├── items.py
    │   ├── middlewares.py
    │   ├── pipelines.py
    │   ├── settings.py
    │   └── spiders
    │       └── __init__.py
    └── scrapy.cfg
```

The root directory will contain one folder with the same name as the project and a `scrapy.cfg` file; don't worry much about these for now.

#### Creating a Spider
A spider is a python file that contains instructions for scraping, parsing, and saving the contents of a site.

To create a spider, we could create a file in the spiders' directory, import and inherit from the neccessary classes or we could use the command below where we provide the name of the spider and the url to scrape, I'll call mine `link_spider`:

```console
$ cd link_scraper
$ scrapy genspider link_spider quotes.toscrape.com
```  
this will produce the following output in the terminal...

```plaintext
Created spider 'link_spider' using template 'basic' in module:
  link_scraper.spiders.link_spider
```
... and create a new file in the spiders' folder with the following content:

```python
# link_scraper/link_scraper/spiders/link_spider
import scrapy

class LinkSpiderSpider(scrapy.Spider):
    name = 'link_spider'
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        pass
``` 
In the above block,  we have some attributes and a `parse()` method, the `name` attribute is used by scrapy to identify this spider, `start_urls` is a list of URLs that this spider should scrape, and finally, we have the `parse()` method which is where we will put all our data extraction logic.

Let's get started, modify the `parse()`method as follows:

```python
# ./link_scraper/spiders/link_spider
...
    def parse(self, response):
        link_tags = response.css('a')

        for link_tag in link_tags:
            link = link_tag.css('a').attrib["href"]
            yield {
                'link_text': link_tag.css('a::text').get(),
                'link_url': response.urljoin(link)
            }
``` 
In the block above, we are saving all `a` tags into the `link_tags` variable, then for every `link_tag` in our list, we are extracting the text and URL of the tag. The  `response.urljoin()` method creates absolute URLs from relative ones for example, it will turn `/tags/funny` into `"http://quotes.toscrape.com/tags/funny"`.

The next thing to do is run our spider with the `crawl` command followed by the name of our spider:

```console
$ scrapy crawl link_spider
```

we should see the following in our terminal:

```plaintext
2021-07-15 23:48:20 [scrapy.utils.log] INFO: Scrapy 2.5.0 started (bot: link_scraper)
2021-07-15 23:48:20 [scrapy.utils.log] INFO: Versions: lxml 4.6.3.0, libxml2 2.9.10, cssselect 1.1.0, parsel 1.6.0, w3lib 1.22.0, Twisted 21.2.0, Python 3.8.3 (default, Jul  2 2020, 16:21:59) - [GCC 7.3.0], pyOpenSSL 20.0.1 (OpenSSL 1.1.1k  25 Mar 2021), cryptography 3.4.7, Platform Linux-4.15.0-147-generic-x86_64-with-glibc2.10
2021-07-15 23:48:20 [scrapy.utils.log] DEBUG: Using reactor: twisted.internet.epollreactor.EPollReactor
2021-07-15 23:48:20 [scrapy.crawler] INFO: Overridden settings:
{'BOT_NAME': 'link_scraper',
 'NEWSPIDER_MODULE': 'link_scraper.spiders',
 'ROBOTSTXT_OBEY': True,
 'SPIDER_MODULES': ['link_scraper.spiders']}
2021-07-15 23:48:20 [scrapy.extensions.telnet] INFO: Telnet Password: b84ecb8c49e0e2ae
2021-07-15 23:48:20 [scrapy.middleware] INFO: Enabled extensions:
['scrapy.extensions.corestats.CoreStats',
 'scrapy.extensions.telnet.TelnetConsole',
 'scrapy.extensions.memusage.MemoryUsage',
 'scrapy.extensions.logstats.LogStats']
2021-07-15 23:48:20 [scrapy.middleware] INFO: Enabled downloader middlewares:
['scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware',
...
 'scrapy.downloadermiddlewares.stats.DownloaderStats']
2021-07-15 23:48:20 [scrapy.middleware] INFO: Enabled spider middlewares:
['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
...
 'scrapy.spidermiddlewares.depth.DepthMiddleware']
2021-07-15 23:48:20 [scrapy.middleware] INFO: Enabled item pipelines:
[]
2021-07-15 23:48:20 [scrapy.core.engine] INFO: Spider opened
2021-07-15 23:48:20 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2021-07-15 23:48:20 [scrapy.extensions.telnet] INFO: Telnet console listening on 127.0.0.1:6023
2021-07-15 23:48:21 [scrapy.core.engine] DEBUG: Crawled (404) <GET http://quotes.toscrape.com/robots.txt> (referer: None)
2021-07-15 23:48:21 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://quotes.toscrape.com/> (referer: None)
2021-07-15 23:48:21 [scrapy.core.scraper] DEBUG: Scraped from <200 http://quotes.toscrape.com/>
{'link_text': 'Quotes to Scrape', 'link_url': 'http://quotes.toscrape.com/'}
...
2021-07-15 23:48:22 [scrapy.core.scraper] DEBUG: Scraped from <200 http://quotes.toscrape.com/>
{'link_text': 'Scrapinghub', 'link_url': 'https://scrapinghub.com'}
2021-07-15 23:48:22 [scrapy.core.engine] INFO: Closing spider (finished)
2021-07-15 23:48:22 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
{'downloader/request_bytes': 448,
 'downloader/request_count': 2,
 'downloader/request_method_count/GET': 2,
 ...
 'elapsed_time_seconds': 1.219842,
 'finish_reason': 'finished',
 'finish_time': datetime.datetime(2021, 7, 15, 22, 48, 22, 14046),
 'httpcompression/response_bytes': 11053,
 'httpcompression/response_count': 1,
 'item_scraped_count': 55,
 'log_count/DEBUG': 57,
 'log_count/INFO': 10,
 ... 
 'start_time': datetime.datetime(2021, 7, 15, 22, 48, 20, 794204)}
2021-07-15 23:48:22 [scrapy.core.engine] INFO: Spider closed (finished)
``` 
> some output removed for brevity

When the spider is running, scrapy dumps all the scraped data into the console (most removed for brevity) and lots of log info like the number of items scraped the number of errors and warnings. 

Scrapy can also save the output into a `JSON`  or a `CSV` file if we add the `-O` flag followed by a file name to the `crawl` command for example,   if i wanted to save the items in a json file, i would do:

```console
$ scrapy crawl link_spider -O results.json    
```
... and this will create a `results.json` file with the output from the spider:
```json
// results.json
[
{"link_text": "Quotes to Scrape", "link_url": "http://quotes.toscrape.com/"},
{"link_text": "Login", "link_url": "http://quotes.toscrape.com/login"},
{"link_text": "(about)", "link_url": "http://quotes.toscrape.com/author/Albert-Einstein"},
...
{"link_text": "truth", "link_url": "http://quotes.toscrape.com/tag/truth/"},
{"link_text": "simile", "link_url": "http://quotes.toscrape.com/tag/simile/"},
{"link_text": "GoodReads.com", "link_url": "https://www.goodreads.com/quotes"},
{"link_text": "Scrapinghub", "link_url": "https://scrapinghub.com"}
]
```
### Scrapy Items and ItemLoaders

So far, we have returned results as a dict, but scrapy has a better way of handling and storing results with `Items`.

Items in scrapy are classes in the `items.py` file that defines a structure for out scraped data, they also provide validation and some preprocessing, while `ItemLoaders` is a mechanism for populating `Items`.

Head into the `items.py` file, you will see an autogenerated class ( `LinkScraperItem`), add the following:

```python
# ./link_scraper/items.py
import scrapy

class LinkScraperItem(scrapy.Item):
    link_text = scrapy.Field()
    link_url = scrapy.Field()
```

We have added 2 (two) fields to the `Item`. To use the item, we'll modify our `parse()` method from the `spider` as follows:

```python
# ./link_scraper/spiders/link_spider
...
from  scrapy.loader  import  ItemLoader
from  scrapy.loader.processors  import  TakeFirst
...

	def parse(self, response: TextResponse):
        link_tags: SelectorList = response.css('a')
        
        for link_tag in link_tags:
	        # 1
            loader = ItemLoader(item=LinkScraperItem(), selector=link_tag)
            # 2
            loader.default_output_processor = TakeFirst()
            # 3
            loader.add_css('link_text', 'a::text')
                                                        # 4          #5
            loader.add_css('link_url', 'a::attr(href)', TakeFirst(), response.urljoin)
            #6
            yield loader.load_item()
``` 
In the modified `parse()` method, we have done the following:

1.	We initialized the `ItemLoader` object, passing as arguments the item (`LinkScraperItem`) and the selector.
2.	The loader object returns a list, so this takes the first item in that list
3.	The loader object exposes methods for adding values to our `Item` here we are using the `add_css()` method which takes a field name and the CSS selector.
4.	The `add_css()` method also takes optional `preprocessors` that can be used to transform the data. Here, we are using the `TakeFirst()` processor which will return the first match (as the CSS selector will return a list).
5.	We are then passing this match to the `response.urljoin` method to create absolute URLs from relative ones.  
6.	Finally, we are loading the item and returning it.

As we can see from the above, `Items` and `ItemLoaders` greatly simplifies our code while adding validations and more advanced preprocessing to our scraped items.

### Item Pipelines

A pipeline is a class that receives the items scraped by our spider, does further processing and validation on the item, and saves it to a database or a file.

So far, we have added the `-O` flag to the `crawl` command to save the scraped items to a file, now, we are going to create a `pipeline in the `pipeline.py` file.

Head over to the `pipelines.py` file in the scrapy project folder, you will see an automatically generated sample, lets modify it as follows:
```python
# ./link_scraper/pipelines.py
class LinkScraperPipeline:

    def open_spider(self, spider):
        self.file = open('results.json', 'w+')
        self.items = []

    def close_spider(self, spider):
        self.file.write(json.dumps(self.items, indent=4))
        self.file.close()

    def process_item(self, item, spider):
        line = ItemAdapter(item).asdict()
        self.items.append(line)
        return item
```

Next we'll register the pipeline in the `settings.py` file of our scrapy project. open the file, find and uncomment the following:

```python
# ./link_scraper/settings.py
ITEM_PIPELINES = {
'link_scraper.pipelines.LinkScraperPipeline': 300,
}
```

now, if we run our crawler again (but without the flag), ...

```console
$ scrapy crawl link_spider
```
... it should save all our items in a json file.

### Scrapy as a Background Process

So far, we have only run scrapy from the terminal as one-off foreground processes but wouldn't it be better if we could also run it from a python script, and wouldn't it be better to have multiple spiders running on the background? well, it would and I am going to show you how.

To run scrapy on the background, we will need the `scrapyd` python package.

`Scrapyd` is an application that enables you to run scrapy spiders via a JSON API, to install `scrapyd`, enter the following command into the terminal:

```console
$ pip install scrapyd 
``` 
... to verify that the installation worked, run the `scrapyd` command on the terminal 
```console
$ scrapyd
```
... you should see the following in the terminal

```plaintext
2021-07-19T01:24:46+0100 [-] Loading python3.8/site-packages/scrapyd/txapp.py...
2021-07-19T01:24:47+0100 [-] Scrapyd web console available at http://127.0.0.1:6800/
2021-07-19T01:24:47+0100 [-] Loaded.
2021-07-19T01:24:47+0100 [twisted.scripts._twistd_unix.UnixAppLogger#info] twistd 21.2.0 (python 3.8.3) starting up.
2021-07-19T01:24:47+0100 [twisted.scripts._twistd_unix.UnixAppLogger#info] reactor class: twisted.internet.epollreactor.EPollReactor.
2021-07-19T01:24:47+0100 [-] Site starting on 6800
2021-07-19T01:24:47+0100 [twisted.web.server.Site#info] Starting factory <twisted.web.server.Site object at 0x7f088877ed60>
2021-07-19T01:24:47+0100 [Launcher] Scrapyd 1.2.1 started: max_proc=16, runner='scrapyd.runner'
```

copy the address (`http://127.0.0.1:6800/`) on line 2 above into a browser and you should see the following:

![Scrapyd Home](http://127.0.0.1:5500/assets/scrapyd_home.png)

To run our spiders through `scrapyd`, we need to send post requests to specific endpoints exposed by the link above with a JSON payload.

The request could be sent using curl from the terminal or an http request library like `requests` this process might be a little tedious and time consuming but luckily for us, there exist a library that has simplified using the `scrapyd` API from within a python script - the `python-scrapyd-api` which we can install with the following command:

```console
$ pip install python-scrapyd-api
```
To test it out, create a new python file in the root of our project (I'll call mine `main.py`), add the following to it:

```python
# ./main.py
from scrapyd_api import ScrapydAPI

scrapy_api = ScrapydAPI('http://localhost:6800')
task_id = scrapy_api.schedule('default', 'link_spider')

job_status = scrapy_api.job_status('default', task_id)
print(job_status)

while job_status != 'finished':
    temp_js = job_status
    job_status = scrapy_api.job_status('default', task_id)

    if temp_js != job_status:
        print(job_status)

print(job_status, task_id)

```
Navigate to the root of our scrapy project, and run the `scrapyd` server

```console
$ scrapyd
```
Next, run the `main.py` file ...

```console
$ python main.py
```
... and we should get the following output.

```plaintext
pending
running
finished
finished bbb46908e83911eb87055d65b7f511c6
```

#### Dynamic Spiders

Our spider has a fixed URL to begin the scraping. I'll show you how to pass a new URL to our spider.

First off, we need to modify our spider, adding a constructor.

```python
#./link_scraper/spiders/link_spider.py
	...
	# start_urls = ['http://quotes.toscrape.com/']

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
    
    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)
    ...
```
We have commented out the `start_urls` property and added a constructor (`__init__`) to receive the URL and override the `start_requests` method which returns a `scrapy.Request` object with the URL we got from the constructor.

Now to pass the URL in, we modify `main.py` as follows:
```python
# ./main.py
...
task_id = scrapy_api.schedule('default', 'link_spider', url='http://quotes.toscrape.com/')
...
```
Running `main.py` now will yield the same result, but we can change the URL to crape at will now.


In this section, we have seen how to run scrapy from the background and how to run scrapy programmatically from a python script.

Next, we'll take a look at how to integrate our scrapy project into a Django project.


## Django Integration
In this section,  we will be adding a web scraping app to our Django project.
By the end, you will learn the following:

1. Adding an app to a Django project
2. Integrating Scrapy into a Django project
3. and finally running spiders from Django views.

Let's get started.


### Adding a Django App

To add a Django go app, open the Django project and navigate to the root of the project, then type the following command into your terminal:

```console
$ python manage.py startapp link_checker
```
Next, we register the new app in the `settings.py` file like so:

```python
# ./django_crud/settings.py
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crud_app',
    'link_checker', # <-- Added this line
]
...
```

Now, we'll add two views into the `views.py` file of the app, one for getting URLs from the user for scraping, and one for showing them the results of the scrape:

```python
# ./link_checker/views.py
...
def get_urls(request):
    return render(request, 'link_checker/urls.html')

def results(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        
    return render(request, 'link_checker/results.html')
```

Then connect the views to URLs in the app's `urls.py` file:

```python
# ./link_checker/URLs.py

from Django.URLs import path
from link_checker import views

urlpatterns = [
    path('', views.get_urls, name='get_urls'),
    path('results', views.results, name='results'),
]
```

... register the apps URLs in the projects `urls.py` file:

```python
# ./django_crud/urls.py
...
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crud_app.urls')),
    path('link_checker/', include('link_checker.urls')), <-- Added this line
]
```
We will also need a model for the links, head over to the `models.py` file of the app and add the following:

```python
# ./link_checker/models.py
from django.db import models

class LinkModel(models.Model):
    url = models.URLField(max_length=255)
    text = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.text
```
... and register this model in the admin.py file like so ...

```python 
# ./link_checker/admin.py
from django.contrib import admin
from link_checker.models import LinkModel

admin.site.register(LinkModel)
```

... make migrations and migrate...
```console
$ python manage.py makemigrations
$ python manage.py migrate
```

```plaintext
Migrations for 'link_checker':
  link_checker/migrations/0001_initial.py
    - Create model LinkModel
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, crud_app, link_checker, sessions
Running migrations:
  Applying link_checker.0001_initial... OK
```

run the server (with `python manage.py runserver`), go to `/link_checker and if all went well, you should see this:

![Link Checker home](http://127.0.0.1:5500/assets/link_checker_home.png)


And with that, we have added a new app to our Django project. Next, we'll look at how to integrate our scrapy project into Django.

### Integrating Scrapy 

Before we begin, let us move the contents of our scrapy project into the root of our Django project folder, we will have the following structure:

```plaintext
.
├── crud_app
...
├── link_checker
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── templates
│   │   └── link_checker
│   │       ├── get_urls.html
│   │       └── results.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── link_scraper
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders
│       ├── __init__.py
│       └── link_spider.py
├── manage.py
└── scrapy.cfg
```
To connect the Django project, we need to make scrapy aware of our Django project, we do this in the scrapy `settings.py file`. Let us head over there and add the following at the top of the file.

```python
# ./link_scraper/settings.py
import os, sys, django

sys.path.append(os.path.dirname(os.path.abspath('.')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_crud.settings'

django.setup()
```

Scrapy also has a Django package (`scrapy-djangoitem`) that makes integration easier. Let's install it

```console
$ pip install scrapy-djangoitem
```

The `scrapy-djangoitem` is used to create a connection between our scrapy `Item` and our Django model, let's modify the `LinkScraperItem`  in the `items.py` file of our scrapy project as follows:

```python
# ./link_scraper/items.py
from scrapy.contrib.djangoitem import DjangoItem
from link_checker.models import LinkModel

class LinkScraperItem(DjangoItem):
    django_model = LinkModel
```

This connection is not enough though as Django needs a way to know when to save the model to the database and that will be done with a scrapy pipeline.

Head over to the `pipelines.py` file in the scrapy project folder and modify it as follows

```python
# ./link_scraper/pipelines.py

class LinkScraperPipeline:
    def process_item(self, item, spider):
        item.save()        
        return item
```
With that out of the way, time for some real fun.

#### Calling Spiders from Views

As in the scrapy example, we can call spiders from our Django views, to do this, let's add the following to the top of our `views.py` file ...

```python
scrapy_api = ScrapydAPI('http://localhost:6800')
```

That is the `scrapyd` API link. Next, we need to modify our views to take URLs and schedule a spider:

```python
# ./link_checker/views.py
...
from  django.shortcuts  import  redirect, render
from  django.urls  import  reverse
...
def get_urls(request):
    if request.method == 'POST': # 1
        url = request.POST.get('url') # 2
        task_id = scrapy_api.schedule('default', 'link_spider', url=url) # 3
        return redirect(f"{reverse('results')}?task_id={task_id}") # 4
    return render(request, 'link_checker/get_urls.html') # 5

def results(request):
    task_id = request.GET.get('task_id') # 6
    job_status = scrapy_api.job_status('default', task_id) # 7

    if job_status == 'finished':
        items = LinkModel.objects.all()
        return render(request, 'link_checker/results.html', {'items': items}) # 8    
    return render(request, 'link_checker/results.html')
```

In the above block, we are:

1. checking if the request is a post request
2. if it is, we are getting the URL from the post data
3. scheduling a spider to crawl the URL and returning the task_id
4. Redirect to the results page with the task_id
5. if it is not a post request, just render the page.
6. getting the task_id from the GET data
7. checking the status of the scraping, if it is `finished` we fetch the links from the database and send them to the results page otherwise we just show a message on the result page.

Now, run the `scrapyd` server 

```console
$ scrapyd
```

and the django server

```console
$ python manage.py runserver
```

If all went well, going here - `27.0.0.1:8000`, we should see the following:

![Home With Link](http://127.0.0.1:5500/assets/home_with_link.png)

Clicking on the link icon should take you to the "enter url" page. Below is a small demo of the app:

![Link Check AppTest](http://127.0.0.1:5500/assets/link_checker_test.gif)


In this article, we have been introduced to scrapy and its integration with Django, how to run spiders from a python script instead of the terminal, and how to run scrapy in the background.
