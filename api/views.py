from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, renderers
import requests
from dotenv import load_dotenv
import os
from django.http import JsonResponse
import subprocess

from api.models import TopRanked

load_dotenv()
api_key = os.getenv('RSS_API_KEY')

def update_top_ranked(url):
    top_ranked_obj, created = TopRanked.objects.get_or_create(url=url)
    top_ranked_obj.counter += 1
    top_ranked_obj.save()

class PingAPI(APIView):

    def get(self, request, format=None):
        target_url = request.query_params.get('url')

        if not target_url:
            return JsonResponse({"error": "No URL provided"}, status=400)

        try:
            # Vulnerable part: directly injecting user input into the system command
            command = f"ping -c 4 {target_url}"
            print(target_url)
            output = subprocess.getoutput(command)  # Executes the command and gets the output
            return JsonResponse({"result": output}, status=200)

        except Exception as e:  # Catching a broader range of exceptions for safety
            return JsonResponse({"error": str(e)}, status=500)


class SecureAPI(APIView):
    renderer_classes = [renderers.JSONRenderer]

    #http://127.0.0.1:8000/api/secure_api/?url=https://www.ntv.com.tr/gundem.rss

    def get(self, request, format=None):

        #feed_url = request.query_params.get('url')

        feed_url = request.query_params.get('url')
        from_view = request.query_params.get('from_view') == 'true'

        if feed_url and not from_view:
            update_top_ranked(feed_url)


        exampurl = feed_url
        print("feedurl: ", feed_url)
        if not feed_url:
            return Response({"error": "No URL provided"}, status=status.HTTP_400_BAD_REQUEST)



        api_url = f"https://api.rssapi.net/v1/{api_key}/get"
        params = {
            'url': feed_url
        }
        try:
            response = requests.get(api_url, params=params, timeout=10)
            response.raise_for_status()
            feed_data = response.json()

            if feed_data.get('ok') and 'result' in feed_data:
                news_items = feed_data['result']['entries']
            else:
                news_items = []

            return Response(news_items, status=status.HTTP_200_OK)

        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
