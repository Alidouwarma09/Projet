# Site/urls.py
from django.urls import path

from Site import views
from Site.views import Index

app_name = 'site'

urlpatterns = [
    path('', Index, name='index'),
    path('publication/<int:pk>/', views.publication_detail, name='publication_detail'),
]
