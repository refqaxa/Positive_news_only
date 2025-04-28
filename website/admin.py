from django.contrib import admin
from .models import User, NewsArticle, Favorite, Preferences

admin.site.register(User)
admin.site.register(NewsArticle)
admin.site.register(Favorite)
admin.site.register(Preferences)
