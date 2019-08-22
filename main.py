import os
import slack
import tutti
import re
import spotipy
import spotipy.util as util
import redis

SLACK_API_TOKEN = os.environ['SLACK_API_TOKEN']
SPOTIFY_USERNAME = os.environ['SPOTIFY_USERNAME']
SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
SPOTIFY_REDIRECT_URL = os.environ['SPOTIFY_REDIRECT_URL']

PLAYLIST_ID = '5VnRiJPPpcQJNQpbak8XDB'
SLACK_CHANNEL_NAME = 'tutti'

r = redis.Redis(host='localhost', port=6379, password=None)
spotify_tokens = r.get('tokens').decode('utf-8')
with open('.cache-' + SPOTIFY_USERNAME, 'w') as f:
    f.write(spotify_tokens)


client = slack.WebClient(token=SLACK_API_TOKEN)

channel_id = tutti.get_channel_id(client, SLACK_CHANNEL_NAME)
messages = tutti.get_channel_messages(client, channel_id)

if len(messages) == 0:
    print('No new messages found')
    quit()

bot_tracks = tutti.get_bot_message_tracks(messages)
user_tracks = tutti.get_user_message_tracks(messages)
all_tracks = bot_tracks + user_tracks

username = SPOTIFY_USERNAME
scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope, 
                                    client_id=SPOTIFY_CLIENT_ID, 
                                    client_secret=SPOTIFY_CLIENT_SECRET, 
                                    redirect_uri=SPOTIFY_REDIRECT_URL)

sp = spotipy.Spotify(auth=token)
result = sp.user_playlist_add_tracks(user=SPOTIFY_USERNAME, playlist_id=PLAYLIST_ID, tracks=all_tracks)
print(result)
