import logging
from django.shortcuts import render
import requests
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('RSS_API_KEY')


def latest(request):
    api_url = f"https://api.rssapi.net/v1/{api_key}/get"
    params = {
        'url': 'https://www.nasa.gov/rss/dyn/breaking_news.rss'
    }

    try:
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        feed_data = response.json()

        if feed_data.get('ok') and 'result' in feed_data:
            news_items = feed_data['result']['entries']
        else:
            news_items = []
    except requests.RequestException as e:
        # Log the error
        logging.error(f"Request error: {str(e)}")
        news_items = []

    context = {
        'news_items': news_items
    }

    return render(request, 'base/latest.html', context)
def index(request):
    return render(request, 'base/index.html')

def sport(request):
    return render(request, 'base/sport.html')

def economy(request):
    return render(request, 'base/economy.html')

def magazine(request):
    return render(request, 'base/magazine.html')

def search(request):
    return render(request, 'base/search.html')