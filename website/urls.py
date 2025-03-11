from django.urls import path
from .views import source_articles, search_articles
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Homepage
    path('source/<str:source>/', source_articles, name='source_articles'), # Artikels bronnen
    path('search/', search_articles, name='search_articles'), # Zoek artikels
    path('article/<str:article_id>/', views.article_detail, name='article_detail'),  # Detailpagina
]