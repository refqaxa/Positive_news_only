from transformers import pipeline
from django.http import Http404
import requests
from .models import NewsArticle


# Use a multilingual sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Articles views
api_key = 'c0ade59a-d8d6-4ca7-afe3-821182107221'  
api_url = 'https://eventregistry.org/api/v1/article/getArticles'

def determine_category(title, description):
    # Lijst met keywords per categorie (uitgebreid)
    sport_keywords = [
        'voetbal', 'tennis', 'hockey', 'sport', 'olympisch', 'wedstrijd', 'kampioen', 
        'toernooi', 'speler', 'atleet', 'ajax', 'psv', 'feyenoord', 'eredivisie', 
        'formule 1', 'f1', 'max verstappen', 'race', 'zwemmen', 'schaatsen', 'wielrennen',
        'tour de france', 'giro', 'vuelta', 'marathon', 'fifa', 'uefa', 'knvb'
    ]
    
    economie_keywords = [
        'economie', 'financieel', 'beurs', 'aandelen', 'bedrijf', 'handel', 'markt',
        'investering', 'bank', 'euro', 'dollar', 'inflatie', 'rente', 'hypotheek',
        'economisch', 'financiën', 'aex', 'nasdaq', 'dow jones', 'werkgelegenheid',
        'werkloosheid', 'prijzen', 'kosten', 'omzet', 'winst', 'verlies', 'faillissement',
        'fusie', 'overname'
    ]
    
    text = (title + ' ' + (description or '')).lower()
    
    # Geef punten voor elke categorie
    sport_score = sum(2 if keyword in title.lower() else 1 for keyword in sport_keywords if keyword in text)
    economie_score = sum(2 if keyword in title.lower() else 1 for keyword in economie_keywords if keyword in text)
    
    # Bepaal de categorie op basis van de hoogste score
    if sport_score > economie_score and sport_score > 0:
        return 'sport'
    elif economie_score > sport_score and economie_score > 0:
        return 'economie'
    return 'algemeen'

def fetch_and_save_articles():
    print("Starting to fetch articles...")  # Debug
    params = {
        'action': 'getArticles',
        'lang': 'nld',  # Taal: Nederlands
        'articlesCount': 100,
        'resultType': 'articles',
        'apiKey': api_key,
    }

    try:
        print("Making API request...")  # Debug
        response = requests.get(api_url, params=params)
        print(f"API Response status: {response.status_code}")  # Debug
        response.raise_for_status()  # Controleer op HTTP-fouten
        data = response.json()
        news_articles = data.get('articles', {}).get('results', [])
        print(f"Found {len(news_articles)} articles from API")  # Debug

        for article in news_articles:
            title = article.get('title', '')
            description = article.get('body', '')
            content = article.get('body', '')
            url = article.get('url', '') 
            image_url = article.get('image', '')
            source = article.get('source', {}).get('title', '')
            published_date = article.get('date', '')

            print(f"\nProcessing article: {title}")  # Debug

            # Bepaal de categorie
            category = determine_category(title, description)
            print(f"Determined category: {category}")  # Debug

            # Combineer titel en beschrijving voor betere analyse
            text_for_analysis = f"{title}. {description}"
            print("Performing sentiment analysis...")  # Debug
            sentiment_result = sentiment_pipeline(text_for_analysis[:512])  # Beperk tot 512 tokens
            sentiment_label = sentiment_result[0]['label']
            sentiment_score = sentiment_result[0]['score']
            print(f"Sentiment analysis result - Label: {sentiment_label}, Score: {sentiment_score}")  # Debug

            # Vertaal sterrenclassificaties naar sentimentlabels
            if sentiment_label in ['3 stars', '4 stars', '5 stars']:  # Aangepast om 3 sterren ook als positief te beschouwen
                sentiment_label = 'POSITIVE'
            elif sentiment_label in ['1 star', '2 stars']:
                sentiment_label = 'NEGATIVE'
            else:
                sentiment_label = 'NEUTRAL'

            # Opslaan bij positieve of neutrale artikelen met een lagere drempelwaarde
            if (
                (sentiment_label == 'POSITIVE' and sentiment_score > 0.3) or  # Verlaagd van 0.4 naar 0.3
                (sentiment_label == 'NEUTRAL' and sentiment_score > 0.3)  # Verlaagd van 0.4 naar 0.3
            ):
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
                        sentiment_score=sentiment_score,
                        category=category
                    )
                    print(f"Saved article in category {category}: {title}")
                else:
                    print(f"Skipped duplicate article: {title}")
            else:
                print(f"Skipped article due to sentiment (label: {sentiment_label}, score: {sentiment_score}): {title}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news articles: {e}")  # Debug
        print(f"Full error details: {str(e)}")  # Debug
