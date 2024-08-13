from googleapiclient.discovery import build
import key

def get_playlist_videos(playlist_id):
    youtube = build('youtube', 'v3', developerKey=key.KEY)
    playlist_items = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,  # You can adjust this value up to 50
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            video_title = item['snippet']['title']
            video_id = item['snippet']['resourceId']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            playlist_items.append({'title': video_title, 'url': video_url})

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return playlist_items