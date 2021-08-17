from django.urls import path
from spellchecker import views

urlpatterns = [
    path('', views.checker, name='checker'),
]