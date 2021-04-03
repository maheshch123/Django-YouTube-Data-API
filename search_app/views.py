import requests

from isodate import parse_duration
from pprint import *
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
def index(request):
    videos = []
    
    if request.method == 'POST':
        
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
                'part' : 'snippet',
                'q' : request.POST['search'],
                'key' : settings.YOUTUBE_DATA_API_KEY,
                'maxResults' : 5,
                'type':'video'
            }
        
        r = requests.get(search_url, params=search_params).json()
        results = r['items']
        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        
        video_params = {
                'key' : settings.YOUTUBE_DATA_API_KEY,
                'part' : 'snippet,contentDetails',
                'id' : ','.join(video_ids),
                'maxResults' : 5
            }
        r = requests.get(video_url, params=video_params).json()
        pprint(r)

        results = r['items']
        for result in results:
            video_data = {
                    'title' : result['snippet']['title'],
                    'id' : result['id'],
                    'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                    'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                    'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                    'channelTitle':result['snippet']['channelTitle'],
                    # 'description': result['snippet']['description']
                }
            videos.append(video_data)
    context = {
        'videos' : videos
    }
    
    return render(request, 'index.html',context)


