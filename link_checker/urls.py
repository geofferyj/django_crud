from django.urls import path

from link_checker import views

urlpatterns = [
    path('', views.get_urls, name='get_url'),
    path('results', views.results, name='results'),
]
