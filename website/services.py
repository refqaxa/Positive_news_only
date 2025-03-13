from transformers import pipeline
from django.http import Http404
import requests
from .models import NewsArticle


# Use a multilingual sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Articles views
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
