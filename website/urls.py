from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Homepage
    path('article/<str:article_id>/', views.article_detail, name='article_detail'),  # Detailpagina
]