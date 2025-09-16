import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')
ID_PLAYLIST = os.getenv('PLAYLIST_ID')

def listar_videos_playlist(playlist_id):
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        videos = []
        next_page_token = None
        
        while True:
            request = youtube.playlistItems().list(
                part='snippet,contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()
            
            for item in response['items']:
                videos.append(item['contentDetails']['videoId'])
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
                
        return videos
        
    except HttpError as e:
        print(f"Erro na API do YouTube: {e}")
        return []

def obter_detalhes_videos(video_ids):
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        detalhes_videos = []
        
        # Processar em lotes de 50 vídeos (limite da API)
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i+50]
            
            request = youtube.videos().list(
                part='snippet,statistics',
                id=','.join(batch)
            )
            response = request.execute()
            
            for item in response['items']:
                snippet = item['snippet']
                statistics = item['statistics']
                
                detalhes_videos.append({
                    'id': item['id'],
                    'titulo': snippet['title'],
                    'descricao': snippet['description'],
                    'data_publicacao': snippet['publishedAt'],
                    'visualizacoes': int(statistics.get('viewCount', 0)),
                    'curtidas': int(statistics.get('likeCount', 0)),
                    'comentarios': int(statistics.get('commentCount', 0)) if 'commentCount' in statistics else 0
                })
        
        return pd.DataFrame(detalhes_videos)
        
    except HttpError as e:
        print(f"Erro na API do YouTube: {e}")
        return pd.DataFrame()