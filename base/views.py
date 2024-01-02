from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
import requests
import os
from dotenv import load_dotenv
import logging
import datetime
from base.models import Comment
from django.db import connection
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required



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


def apiSearch(request):
    custom_url = request.GET.get("custom_url")

    if custom_url:

        feed_data = fetch_data_from_secure_api(custom_url)
    else:
        feed_data = None

    context = {'news_items': feed_data}
    return render(request, 'base/apiSearch.html', context)


def titleSearch(request):
    if request.method == 'GET':
        q = request.GET.get('q', '')  # q parametresini güvenli bir şekilde al


        if q:  # Eğer q varsa ve boş değilse
            # Tüm haber kaynaklarından haberleri çek
            urls = [
                'https://www.ntv.com.tr/gundem.rss',
                'https://www.ntv.com.tr/son-dakika.rss',
                'https://www.ntv.com.tr/spor.rss',
                'https://www.ntv.com.tr/ekonomi.rss',
                'https://www.ntv.com.tr/yasam.rss'
            ]

            filtered_news_items = []

            for url in urls:
                feed_data = fetch_data_from_secure_api(url)


                if feed_data:
                    #print(f"{url} adresinden gelen haber başlıkları:")

                    # Sorguya uyan haber başlıklarını filtrele
                    for item in feed_data:
                        if 'title' in item:
                            pass
                            #print(item['title'])
                        # if 'title' in item and q.lower() in item['title'].lower():
                        #     filtered_news_items.append(item)
                        if 'title' in item and q.lower() in item['title'].lower():
                            filtered_news_items.append(item)
                            print(f"Eşleşen başlık: {item['title']}")

            context = {'filtered_news_items': filtered_news_items}
        else:
            # q parametresi yoksa veya boşsa, boş bir liste döndür
            context = {'news_items': []}

        return render(request, 'base/titleSearch.html', context)


def newsDetail(request):
    news_link = request.GET.get('link', None)

    news_detail = None
    if news_link:
        # Fetch all news
        urls = [
            'https://www.ntv.com.tr/gundem.rss',
            'https://www.ntv.com.tr/son-dakika.rss',
            'https://www.ntv.com.tr/spor.rss',
            'https://www.ntv.com.tr/ekonomi.rss',
            'https://www.ntv.com.tr/yasam.rss'
        ]

        for url in urls:
            feed_data = fetch_data_from_secure_api(url)
            if feed_data:
                # Search for news details by link
                for item in feed_data:
                    if 'link' in item and item['link'] == news_link:
                        news_detail = item
                        break
            if news_detail:
                break

    if request.method == 'POST':
        comment_content = request.POST.get('comment')
        user = request.user
        current_time = datetime.datetime.now()
        sql = "INSERT INTO base_comment (news_link, user_id, created_at, content) VALUES ('%s', '%s', '%s', '%s')" % (news_link, user.id, current_time, comment_content)    
        with connection.cursor() as cursor:
            cursor.executescript(sql)
          

        return redirect(f'/newsDetail/?link={news_link}')

    # Retrieving comments
    comments = Comment.objects.filter(news_link=news_link)

    # Context for rendering
    context = {'news_detail': news_detail, 'comments': comments}
    return render(request, 'base/newsDetail.html', context)




@login_required
def deleteComment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Yalnızca yorumu yapan kullanıcı veya admin yorumu silebilir
    if request.user == comment.user or request.user.is_superuser:
        comment.delete()
        return redirect(f'/newsDetail/?link={comment.news_link}')

    else:
        # Yetkisi olmayan kullanıcılar için hata mesajı göster
        return HttpResponseForbidden('Bu yorumu silme yetkiniz yok.')