from django.shortcuts import render
import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()
api_key = os.getenv('RSS_API_KEY')
secure_api_url = "http://localhost:8000/api/secure_api"  


def fetch_data_from_secure_api(url):
    try:
        response = requests.get(f"{secure_api_url}/?url={url}", timeout=10)
        response.raise_for_status()
        feed_data = response.json()
        return feed_data
    except requests.RequestException as e:
        logging.error(f"Request error to secure API: {str(e)}")
        return None


def index(request):
    url = 'https://www.ntv.com.tr/gundem.rss'
    feed_data = fetch_data_from_secure_api(url)

    if feed_data:
        news_items = feed_data
    else:
        news_items = []

    context = {'news_items': news_items}
    return render(request, 'base/index.html', context)


def latest(request):
    url = 'https://www.ntv.com.tr/son-dakika.rss'
    feed_data = fetch_data_from_secure_api(url)

    if feed_data:
        news_items = feed_data
    else:
        news_items = []

    context = {'news_items': news_items}
    return render(request, 'base/latest.html', context)


def sport(request):
    url = 'https://www.ntv.com.tr/spor.rss'
    feed_data = fetch_data_from_secure_api(url)

    if feed_data:
        news_items = feed_data
    else:
        news_items = []

    context = {'news_items': news_items}
    return render(request, 'base/sport.html', context)

# View to display economy news from the secure API
def economy(request):
    url = 'https://www.ntv.com.tr/ekonomi.rss'
    feed_data = fetch_data_from_secure_api(url)

    if feed_data:
        news_items = feed_data
    else:
        news_items = []

    context = {'news_items': news_items}
    return render(request, 'base/economy.html', context)

def magazine(request):
    url = 'https://www.ntv.com.tr/yasam.rss'
    feed_data = fetch_data_from_secure_api(url)

    if feed_data:
        news_items = feed_data
    else:
        news_items = []

    context = {'news_items': news_items}
    return render(request, 'base/magazine.html', context)


def search(request):
    custom_url = request.GET.get("custom_url")  
    if custom_url:
        feed_data = fetch_data_from_secure_api(custom_url)  
    else:
        feed_data = None

    context = {'news_items': feed_data}
    return render(request, 'base/search.html', context)

