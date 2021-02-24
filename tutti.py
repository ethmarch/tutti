import os
import re
import time

def get_channel_id(client, channel_name):
    response = client.conversations_list(exclude_archived=1)
    channel = [x for x in response['channels'] if x['name'] == channel_name][0]
    return channel['id']

def get_channel_messages(client, channel_id):
    messages = client.conversations_history(channel=channel_id, inclusive=1, oldest=str(round(time.time() - 600)))
    return messages['messages']

def get_bot_message_tracks(messages):
    spotify_bot_messages = [x for x in messages if x.get('bot_id') == 'B9W1JVD2Q']
    track_regex = r'(.*)https:\/\/open.spotify.com\/track\/([A-z0-9]*)(.*)'

    if len(spotify_bot_messages) == 0:
        return []

    track_ids = []
    for message in spotify_bot_messages:
        attachments = message.get('attachments')
        link = attachments[0]['title_link']
        groups = re.search(track_regex, link)
        if groups is not None:
            track_ids.append(groups.group(2))
    
    return track_ids

def get_user_message_tracks(messages):
    track_regex = r'(.*)https:\/\/open.spotify.com\/track\/([A-z0-9]*)(.*)'
    track_ids = []
    for message in messages:
        text = message.get('text')
        groups = re.search(track_regex, text)
        if groups is not None:
            track_ids.append(groups.group(2))
    
    return track_ids


