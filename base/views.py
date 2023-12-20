import logging
from django.shortcuts import render
import requests
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('RSS_API_KEY')

def index(request):
    api_url = f"https://api.rssapi.net/v1/{api_key}/get"
    params = {
        'url': 'https://www.ntv.com.tr/gundem.rss'
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
    return render(request, 'base/index.html', context)


def latest(request):
    api_url = f"https://api.rssapi.net/v1/{api_key}/get"
    params = {
        'url': 'https://www.ntv.com.tr/son-dakika.rss'
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


def sport(request):
    api_url = f"https://api.rssapi.net/v1/{api_key}/get"
    params = {
        'url': 'https://www.ntv.com.tr/spor.rss'
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
    return render(request, 'base/sport.html', context)

def economy(request):
    api_url = f"https://api.rssapi.net/v1/{api_key}/get"
    params = {
        'url': 'https://www.ntv.com.tr/ekonomi.rss'
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

    return render(request, 'base/economy.html', context)

def magazine(request):
    api_url = f"https://api.rssapi.net/v1/{api_key}/get"
    params = {
        'url': 'https://www.ntv.com.tr/yasam.rss'
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
    return render(request, 'base/magazine.html', context)

def search(request):
    api_url = f"https://api.rssapi.net/v1/{api_key}/get"
    params = {
        'url': 'https://www.ntv.com.tr/spor.rss'
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
    return render(request, 'base/search.html', context)