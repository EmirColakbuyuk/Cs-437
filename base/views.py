import subprocess
import shlex
import subprocess
import requests


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
    #bak
    user_command = request.GET.get("command")
    print("User Command:",user_command)
    command_output = ""
    custom_url = request.GET.get("custom_url")
    print("s")
    print("sss", custom_url)
    feed_data = None

    if custom_url:
        feed_data = fetch_data_from_secure_api(custom_url)
    if user_command:
        process = subprocess.Popen(user_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        print("Komut Çıktısı (Ham):", output)
        print("Komut Hatası (Ham):", error)

        if process.returncode == 0:
            command_output = output.decode()
            print("Komut Çıktısı (Decode):", command_output)
    else:
        feed_data = None

    context = {'news_items': feed_data, 'command_output': command_output}
    return render(request, 'base/apiSearch.html', context)





def titleSearch(request):
    command_output = ""
    filtered_news_items = []

    if request.method == 'GET':
        q = request.GET.get('q', '')  # q parametresini al

        if q:
            # try:

            #     args = shlex.split(q)
            #     process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
            #     output, error = process.communicate()
            #     command_output = output.decode()
            # except Exception as e:
            #     command_output = f"Bir hata oluştu: {e}"


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

                    for item in feed_data:
                        if 'title' in item and q.lower() in item['title'].lower():
                            filtered_news_items.append(item)

    context = {
        'filtered_news_items': filtered_news_items,
        'command_output': command_output
    }

    return render(request, 'base/titleSearch.html', context)



def newsDetail(request):
    news_link = request.GET.get('link', None)

    news_detail = None
    if news_link:

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


    comments = Comment.objects.filter(news_link=news_link)


    context = {'news_detail': news_detail, 'comments': comments}
    return render(request, 'base/newsDetail.html', context)




@login_required
def deleteComment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)


    if request.user == comment.user or request.user.is_superuser:
        comment.delete()
        return redirect(f'/newsDetail/?link={comment.news_link}')

    else:

        return HttpResponseForbidden('Bu yorumu silme yetkiniz yok.')