# Site/urls.py
from django.urls import path

from Site.views import Index

app_name = 'site'

urlpatterns = [
    path('', Index, name='index'),
]
