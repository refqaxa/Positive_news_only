from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from .models import NewsArticle
from django.core.paginator import Paginator
from django.http import Http404
import requests
from transformers import pipeline
# from textblob import TextBlob
import pdb

# Use a multilingual sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

api_key = 'c0ade59a-d8d6-4ca7-afe3-821182107221'  
api_url = 'https://eventregistry.org/api/v1/article/getArticles'

def fetch_and_save_articles():
    # print("Funtion start of fetching srticles") # Debugging
    params = {
        'action': 'getArticles',
        # 'keyword': 'goed nieuws',
        'lang': 'nld',  # Taal: Nederlands
        'articlesCount': 100,
        'resultType': 'articles',
        'apiKey': api_key,
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status() # Controleer op HTTP-fouten
        data = response.json()
        news_articles = data.get('articles', {}).get('results', [])

        for article in news_articles:
            # print(article)
            title = article.get('title', '')
            description = article.get('body', '')
            content = article.get('body', '')
            url = article.get('url', '') 
            image_url = article.get('image', '')
            source = article.get('source', {}).get('title', '')
            published_date = article.get('date', '')

             # Combineer titel en beschrijving voor betere analyse
            text_for_analysis = f"{title}. {description}"
            sentiment_result = sentiment_pipeline(text_for_analysis[:512])  # Beperk tot 512 tokens
            sentiment_label = sentiment_result[0]['label']
            sentiment_score = sentiment_result[0]['score']

            # Vertaal sterrenclassificaties naar sentimentlabels
            if sentiment_label in ['4 stars', '5 stars']:
                sentiment_label = 'POSITIVE'
            elif sentiment_label in ['1 star', '2 stars']:
                sentiment_label = 'NEGATIVE'
            else:
                sentiment_label = 'NEUTRAL'
                
            # print(f"Sentiment Label: {sentiment_label}, Sentiment Score: {sentiment_score}")  # Debug

            # Opslaan bij positieve of neutrale artikelen
            if (
                (sentiment_label == 'POSITIVE' and sentiment_score > 0.4) or
                (sentiment_label == 'NEUTRAL' and sentiment_score > 0.4)
            ):
                print("opgeslagen!")
                # Check if article already exists to avoid duplicates
                if not NewsArticle.objects.filter(url=url).exists():
                    NewsArticle.objects.create(
                        title=title,
                        description=description,
                        content=content,
                        url=url,
                        image_url=image_url,
                        source=source,
                        published_date=published_date,
                        sentiment_score=sentiment_score
                    )
                    print(f"Saved positive article: {title}")

    except requests.exceptions.RequestException as e:
            print(f"Fout bij het ophalen van nieuwsberichten: {e}")  # Debug: print foutmelding

def home(request):
    articles_list = NewsArticle.objects.order_by('-published_date')
    sources = NewsArticle.objects.values_list('source', flat=True).distinct()  # Unieke bronnen ophalen
    
    if articles_list.count() == 0:
        return render(request, 'home.html', {'message': 'Geen nieuwsberichten beschikbaar'})

    paginator = Paginator(articles_list, 12)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)

    context = {
        'news_articles': articles,
        'sources': sources
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

def all_sources(request):
    sources = NewsArticle.objects.values_list('source', flat=True).distinct()  # Alle unieke bronnen ophalen
    return render(request, 'all_sources.html', {'sources': sources})


# Task: get artikel detail from database with artikel id

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