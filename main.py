import os
from slack_sdk import WebClient
import tutti
import re
import spotipy
import spotipy.util as util

SLACK_API_TOKEN = os.environ['SLACK_API_TOKEN']
SPOTIFY_USERNAME = os.environ['SPOTIFY_USERNAME']
SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
SPOTIFY_REDIRECT_URL = os.environ['SPOTIFY_REDIRECT_URL']
SPOTIFY_TOKENS = os.environ['SPOTIFY_TOKENS']

PLAYLIST_ID = '5VnRiJPPpcQJNQpbak8XDB'
SLACK_CHANNEL_NAME = 'music'

with open('.cache-' + SPOTIFY_USERNAME, 'w') as f:
    f.write(SPOTIFY_TOKENS)

client = WebClient(token=SLACK_API_TOKEN)

channel_id = tutti.get_channel_id(client, SLACK_CHANNEL_NAME)
messages = tutti.get_channel_messages(client, channel_id)

all_tracks = []
if len(messages) != 0:
    bot_tracks = tutti.get_bot_message_tracks(messages)
    user_tracks = tutti.get_user_message_tracks(messages)
    all_tracks = bot_tracks + user_tracks


if len(all_tracks) != 0:
    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(SPOTIFY_USERNAME, scope, 
                                        client_id=SPOTIFY_CLIENT_ID, 
                                        client_secret=SPOTIFY_CLIENT_SECRET, 
                                        redirect_uri=SPOTIFY_REDIRECT_URL)

    sp = spotipy.Spotify(auth=token)
    result = sp.user_playlist_add_tracks(user=SPOTIFY_USERNAME, playlist_id=PLAYLIST_ID, tracks=all_tracks)
    print(result)
else:
    print('No new tracks found')

