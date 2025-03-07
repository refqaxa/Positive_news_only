from django.shortcuts import render, get_object_or_404
from django.http import Http404
import requests

def home(request):
    api_key = 'c0ade59a-d8d6-4ca7-afe3-821182107221'  # Jouw NewsAPI.ai-sleutel
    url = 'https://eventregistry.org/api/v1/article/getArticles'
    params = {
        'action': 'getArticles',
        'keyword': 'goed nieuws',  # Pas dit aan naar je gewenste zoekwoord
        'lang': 'nld',  # Taal: Nederlands
        'articlesCount': 10,  # Aantal artikelen om op te halen
        'resultType': 'articles',
        'apiKey': api_key,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Controleer op HTTP-fouten
        data = response.json()
        print(f"API-respons: {data}")  # Debug: print de API-respons

        # Haal de artikelen op uit de respons
        news_articles = data.get('articles', {}).get('results', [])
        print(f"Nieuwsberichten: {news_articles}")  # Debug: print de nieuwsberichten

    except requests.exceptions.RequestException as e:
        print(f"Fout bij het ophalen van nieuwsberichten: {e}")  # Debug: print foutmelding
        news_articles = []  # Geef een lege lijst terug bij een fout

    context = {
        'news_articles': news_articles,
    }
    return render(request, 'home.html', context)

def article_detail(request, article_id):
    api_key = 'c0ade59a-d8d6-4ca7-afe3-821182107221'  # Jouw NewsAPI.ai-sleutel
    url = 'https://eventregistry.org/api/v1/article/getArticles'
    params = {
        'action': 'getArticles',
        'articleUri': article_id,  # Gebruik de article_id om het specifieke artikel op te halen
        'apiKey': api_key,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Controleer op HTTP-fouten
        data = response.json()
        print(f"API-respons: {data}")  # Debug: print de API-respons

        # Haal het artikel op uit de respons
        article = data.get('articles', {}).get('results', [])[0]  # Neem het eerste artikel
        print(f"Artikel: {article}")  # Debug: print het artikel

    except (requests.exceptions.RequestException, IndexError) as e:
        print(f"Fout bij het ophalen van het artikel: {e}")  # Debug: print foutmelding
        raise Http404("Artikel niet gevonden")  # Geef een 404-fout als het artikel niet bestaat

    context = {
        'article': article,
    }
    return render(request, 'article_detail.html', context)