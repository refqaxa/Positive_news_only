from django.urls import path
from .views import home, article_detail, source_articles, search_articles, all_sources, register, user_login, user_logout
from .views import user_profile, favorite_articles, toggle_favorite, account_settings_view, source_settings_view


urlpatterns = [
    # artikelen pagina's
    path('', home, name='home'),  # Homepage
    path('source/<str:source>/', source_articles, name='source_articles'), # Artikels bronnen
    path('search/', search_articles, name='search_articles'), # Zoek artikels
    path('article/<str:article_id>/', article_detail, name='article_detail'),  # Detailpagina
    path('all_sources/', all_sources, name='all_sources'),  # Nieuwe pagina voor alle bronnen
    
    # user pagina's
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', user_profile, name='user_profile'),
    path('favorites/', favorite_articles, name='favorite_articles'),
    path('toggle_favorite/<int:article_id>/', toggle_favorite, name='toggle_favorite'),
    path('account-settings/', account_settings_view, name='account_settings'),
    path('source-settings/', source_settings_view, name='source_settings'),
]