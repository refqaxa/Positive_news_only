from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, UpdateProfileForm
from .models import NewsArticle, User, Favorite
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
import requests
from django.contrib import messages


# Articles views
def home(request):
    articles_list = NewsArticle.objects.order_by('-published_date')
    categories = [{'id': cat[0], 'name': cat[1]} for cat in NewsArticle.CATEGORY_CHOICES]
    
    if articles_list.count() == 0:
        return render(request, 'home.html', {'message': 'Geen nieuwsberichten beschikbaar'})

    paginator = Paginator(articles_list, 12)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)

    context = {
        'news_articles': articles,
        'categories': categories
    }
    return render(request, 'home.html', context)

def category_articles(request, category):
    articles_list = NewsArticle.objects.filter(category=category).order_by('-published_date')
    categories = [{'id': cat[0], 'name': cat[1]} for cat in NewsArticle.CATEGORY_CHOICES]

    if not articles_list.exists():
        return render(request, 'home.html', {
            'message': f'Geen artikelen gevonden in de categorie: {dict(NewsArticle.CATEGORY_CHOICES).get(category, category)}',
            'categories': categories
        })

    paginator = Paginator(articles_list, 12)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)

    context = {
        'news_articles': articles,
        'categories': categories,
        'current_category': category
    }
    return render(request, 'home.html', context)

# Artikelen ophalen per nieuwsbron
def source_articles(request, source):
    articles_list = NewsArticle.objects.filter(source=source).order_by('-published_date')
    sources = NewsArticle.objects.values_list('source', flat=True).distinct()

    if not articles_list.exists():
        return render(request, 'home.html', {'message': f'Geen artikelen gevonden voor bron: {source}'})

    paginator = Paginator(articles_list, 10)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)

    context = {
        'news_articles': articles,
        'sources': sources,
        'current_source': source
    }
    return render(request, 'home.html', context)

def all_sources(request):
    sources = NewsArticle.objects.values_list('source', flat=True).distinct()  # Alle unieke bronnen ophalen
    return render(request, 'all_sources.html', {'sources': sources})

# Zoekfunctie voor artikelen op titel
def search_articles(request):
    query = request.GET.get('q')
    static_sources = ['Nieuwsbron 1', 'Nieuwsbron 2', 'Nieuwsbron 3', 'Nieuwsbron 4', 'Nieuwsbron 5']
    
    # Als er geen bronnen in de database zijn, gebruik dan de statische bronnen
    sources = NewsArticle.objects.values_list('source', flat=True).distinct()
    if not sources:
        sources = static_sources

    if query:
        articles_list = NewsArticle.objects.filter(title__icontains=query).order_by('-published_date')
    else:
        articles_list = NewsArticle.objects.none()

    paginator = Paginator(articles_list, 10)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)

    context = {
        'news_articles': articles,
        'sources': sources,
        'query': query
    }
    return render(request, 'home.html', context)

def article_detail(request, article_id):
    # Haal het artikel uit de database
    article = get_object_or_404(NewsArticle, article_id=article_id)
     # Check if the user is authenticated
    if request.user.is_authenticated:
        # Check if the article is favorited by the current user
        is_favorited = Favorite.objects.filter(user=request.user, article=article).exists()
    else:
        # If the user is not logged in, we set `is_favorited` to False
        is_favorited = False
    context = {
        'article': article,
        'is_favorited': is_favorited,  # Pass this variable to the template
    }
    return render(request, 'article_detail.html', context)

# User views
# Register
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account succesvol aangemaakt! Je kunt nu inloggen.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# login
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Debug print
            print(f"Attempting to authenticate user: {username}")
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                print(f"User authenticated successfully: {user.username}")
                login(request, user)
                return redirect('home')
            else:
                print(f"Authentication failed for user: {username}")
                form.add_error(None, 'Je gebruikersnaam en wachtwoord komen niet overeen')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# User profile that requires login
@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

# Logout
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

# User favorite articles, settings and soruces prefrences
@login_required
def favorite_articles(request):
    favorites = []
    if request.user.is_authenticated:
        # Get all favorites for the logged-in user and include the article related to each favorite
        favorites = Favorite.objects.filter(user=request.user).select_related('article')

    context = {
        'favorites': favorites,
    }
    return render(request, 'favorites.html', context)


@login_required
def toggle_favorite(request, article_id):
    article = get_object_or_404(NewsArticle, article_id=article_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, article=article)
    
    if not created:
        favorite.delete()
        is_favorited = False
    else:
        is_favorited = True
    
    if request.headers.get('HX-Request'):
        return render(request, 'favorite_button.html', {
            'article': article,
            'is_favorited': is_favorited
        })
    
    # Check if the request came from the favorites page
    referer = request.META.get('HTTP_REFERER', '')
    if 'favorites' in referer:
        return redirect('favorites')
    
    return redirect('article_detail', article_id=article_id)

@login_required
def account_settings_view(request):
    return render(request, 'account_settings.html')

@login_required
def source_settings_view(request):
    return render(request, 'source_settings.html')
