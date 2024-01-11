import subprocess
import shlex
import subprocess
from email.utils import parsedate_to_datetime

import requests


from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
import requests
import os
from dotenv import load_dotenv
import logging
import datetime

from api.models import TopRanked
from base.models import Comment
from django.db import connection
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import News


load_dotenv()
api_key = os.getenv('RSS_API_KEY')
secure_api_url = "http://localhost:8000/api/secure_api"


import requests
import logging
from django.utils.dateparse import parse_datetime
from .models import News

logger = logging.getLogger(__name__)

#that part saving news to database from api, it is good because api is so protective. If news stored in database, it is
#very common case an also there can be a chance for SQL INJECTION and COMMAND LINE INJECTION
def fetch_data_from_secure_api(url, from_view=False):
    try:
        params = {'url': url}
        if from_view:
            params['from_view'] = 'true'
        response = requests.get(f"{secure_api_url}/", params=params, timeout=10)
        #print(response.status_code)
        #print(response.text)
        response.raise_for_status()
        feed_data = response.json()
        #print("keke selam", url)

        if 'gundem' in url:
            category = 'gundem'
        if 'son-dakika' in url:
            category = 'son-dakika'
        if 'spor' in url:
            category = 'spor'
        if 'ekonomi' in url:
            category = 'ekonomi'
        if 'yasam' in url:
            category = 'yasam'


        for item in feed_data:
            published_time_str = item.get('time')
            published_time = parsedate_to_datetime(published_time_str) if published_time_str else None
            #print("keke selam", item.published_time)
            news_url = item.get('link', 'No URL provided')
            logging.info(f"Processing news item with URL: {news_url}")

            news, created = News.objects.get_or_create(
                title=item['title'],
                defaults={
                    'description': item.get('description', ''),
                    'content': item['content']['text'],
                    'link': item['link'],
                    'image_url': item['image']['url'],
                    'published_time': published_time,
                    'category': category
                }
            )

            if not created:

                pass

        return feed_data

    except requests.RequestException as e:
        logging.error(f"Request error to secure API: {str(e)}")
        return None



def index(request):
    # url = 'https://www.ntv.com.tr/gundem.rss'
    # feed_data = fetch_data_from_secure_api(url, from_view=True)
    #
    # if feed_data:
    #     news_items = feed_data
    # else:
    #     news_items = []

    # test_date = "Thu, 11 Jan 2024 14:17:00 +0000"
    # converted_date = parsedate_to_datetime(test_date)
    # print(converted_date)

    url = 'https://www.ntv.com.tr/gundem.rss'
    feed_data = fetch_data_from_secure_api(url, from_view=True)



    news_items = News.objects.filter(category='gundem').order_by('-published_time')
    context = {'news_items': news_items}
    return render(request, 'base/index.html', context)


def latest(request):
    url = 'https://www.ntv.com.tr/son-dakika.rss'
    feed_data = fetch_data_from_secure_api(url, from_view=True)
    #
    # if feed_data:
    #     news_items = feed_data
    # else:
    #     news_items = []
    news_items = News.objects.filter(category='son-dakika').order_by('-published_time')


    context = {'news_items': news_items}
    return render(request, 'base/latest.html', context)


def sport(request):
    url = 'https://www.ntv.com.tr/spor.rss'
    feed_data = fetch_data_from_secure_api(url, from_view=True)
    #
    # if feed_data:
    #     news_items = feed_data
    # else:
    #     news_items = []
    news_items = News.objects.filter(category='spor').order_by('-published_time')

    context = {'news_items': news_items}
    return render(request, 'base/sport.html', context)


def economy(request):
    url = 'https://www.ntv.com.tr/ekonomi.rss'
    feed_data = fetch_data_from_secure_api(url, from_view=True)
    #
    # if feed_data:
    #     news_items = feed_data
    # else:
    #     news_items = []

    news_items = News.objects.filter(category='ekonomi').order_by('-published_time')

    context = {'news_items': news_items}
    return render(request, 'base/economy.html', context)

def magazine(request):
    url = 'https://www.ntv.com.tr/yasam.rss'
    feed_data = fetch_data_from_secure_api(url, from_view=True)
    #
    # if feed_data:
    #     news_items = feed_data
    # else:
    #     news_items = []

    news_items = News.objects.filter(category='yasam').order_by('-published_time')

    context = {'news_items': news_items}
    return render(request, 'base/magazine.html', context)



def apiSearch(request):
    top_ranked_items = TopRanked.objects.order_by('-counter')[:5]
    context = {'top_ranked_items': top_ranked_items}


    return render(request, 'base/apiSearch.html', context)





def titleSearch(request):
    command_output = ""
    filtered_news_items = []

    if request.method == 'GET':
        q = request.GET.get('q', '')
        if q and q is not None:
            filtered_news_items = News.objects.filter(title__contains=q)

        # if q:
        #     # try:
        #
        #     #     args = shlex.split(q)
        #     #     process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        #     #     output, error = process.communicate()
        #     #     command_output = output.decode()
        #     # except Exception as e:
        #     #     command_output = f"hata : {e}"
        #
        #
        #     urls = [
        #         'https://www.ntv.com.tr/gundem.rss',
        #         'https://www.ntv.com.tr/son-dakika.rss',
        #         'https://www.ntv.com.tr/spor.rss',
        #         'https://www.ntv.com.tr/ekonomi.rss',
        #         'https://www.ntv.com.tr/yasam.rss'
        #     ]
        #
        #     for url in urls:
        #         feed_data = fetch_data_from_secure_api(url, from_view=True)
        #
        #         if feed_data:
        #
        #             for item in feed_data:
        #                 if 'title' in item and q.lower() in item['title'].lower():
        #                     filtered_news_items.append(item)



    context = {
        'filtered_news_items': filtered_news_items,
        'command_output': command_output
    }

    return render(request, 'base/titleSearch.html', context)


#VULNERABLE PART
def newsDetail(request):
    # news_link = request.GET.get('link', None)
    #
    # news_detail = None
    # if news_link:
    #
    #     urls = [
    #         'https://www.ntv.com.tr/gundem.rss',
    #         'https://www.ntv.com.tr/son-dakika.rss',
    #         'https://www.ntv.com.tr/spor.rss',
    #         'https://www.ntv.com.tr/ekonomi.rss',
    #         'https://www.ntv.com.tr/yasam.rss'
    #     ]
    #
    #     for url in urls:
    #         feed_data = fetch_data_from_secure_api(url, from_view=True)
    #         if feed_data:
    #
    #             for item in feed_data:
    #                 if 'link' in item and item['link'] == news_link:
    #                     news_detail = item
    #                     break
    #         if news_detail:
    #             break

    news_link = request.GET.get('link', None)

    if news_link:

        news_detail = get_object_or_404(News, link=news_link)
    else:
        news_detail = None


    #as you may see there is an sql command for the saving of comments, that is a big vulnerability because it can be
    #exploitable with sql_ınjection. So it is more safer with django save command. Also as you may se there is an
    #executescript method used, it allows sqlite to do multiple progress like ınsert or delete at the same time
    if request.method == 'POST':
        comment_content = request.POST.get('comment')
        user = request.user
        current_time = datetime.datetime.now()
        sql = "INSERT INTO base_comment (news_link, user_id, created_at, content) VALUES ('%s', '%s', '%s', '%s')" % (news_link, user.id, current_time, comment_content)    
        with connection.cursor() as cursor:
            cursor.executescript(sql)
          

        return redirect(f'/newsDetail/?link={news_link}')


    comments = Comment.objects.filter(news_link=news_link)


    context = {'news_detail': news_detail, 'comments': comments}
    return render(request, 'base/newsDetail.html', context)



#IT IS PROTECTIVE AREA HOWEVER WITH THE VULNERABLE OF SQL_INJECTION, THAT PART CAN BE EXPLOIT
@login_required
def deleteComment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)


    if request.user == comment.user or request.user.is_superuser:
        comment.delete()
        return redirect(f'/newsDetail/?link={comment.news_link}')

    else:

        return HttpResponseForbidden('Bu yorumu silme yetkiniz yok.')