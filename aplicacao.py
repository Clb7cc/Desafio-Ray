import os
from googleapiclient.discovery import build
import pandas as pd

# Configurações da API
CHAVE_API = os.getenv("YOUTUBE_API_KEY", "SUA_CHAVE_AQUI")
ID_PLAYLIST = os.getenv("YOUTUBE_PLAYLIST_ID", "PLAYLIST_ID_AQUI")  
YOUTUBE = build('youtube', 'v3', developerKey=CHAVE_API)

def listar_videos_playlist(id_playlist):
    ids_videos = []
    token = None
    
    while True:
        resposta = YOUTUBE.playlistItems().list(
            part='contentDetails',
            playlistId=id_playlist,
            maxResults=50,
            pageToken=token
        ).execute()
        
        for item in resposta.get('items', []):
            ids_videos.append(item['contentDetails']['videoId'])
        
        token = resposta.get('nextPageToken')
        if not token:
            break
    
    return ids_videos

def obter_detalhes_videos(ids_videos):
    registros = []
    
    for i in range(0, len(ids_videos), 50):
        lote = ids_videos[i:i+50]
        resposta = YOUTUBE.videos().list(
            part='snippet,statistics,contentDetails',
            id=','.join(lote)
        ).execute()
        
        for item in resposta.get('items', []):
            s = item.get('snippet', {})
            e = item.get('statistics', {})
            c = item.get('contentDetails', {})
            
            registro = {
                'id_video': item.get('id'),
                'titulo': s.get('title'),
                'data_publicacao': s.get('publishedAt'),
                'visualizacoes': int(e.get('viewCount', 0)),
                'curtidas': int(e.get('likeCount', 0)) if e.get('likeCount') else None,
                'comentarios': int(e.get('commentCount', 0)) if e.get('commentCount') else None,
            }
            registros.append(registro)
    
    return pd.DataFrame(registros)

def principal():
    ids = listar_videos_playlist(ID_PLAYLIST)
    print(f"Vídeos encontrados: {len(ids)}")
    return obter_detalhes_videos(ids)

if __name__ == "__main__":
    principal()