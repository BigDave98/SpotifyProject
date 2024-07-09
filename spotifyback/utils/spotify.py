# -*- coding: utf-8 -*-
import spotipy
from flask import url_for, session
from spotipy.oauth2 import SpotifyOAuth
import time

import csv
import os

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id='07ea87a0e0c34aa28f6550d4d2f612dc',
        client_secret='04bfced91d2349d49d0d840660ccb0ba',
        redirect_uri=url_for('authorize', _external = True),
        scope="user-library-read"
    )

# Checks to see if token is valid and gets a new token if not
def get_token(session):
    token_valid = False
    token_info = session.get("token_info", {})
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    now = int(time.time())
    is_expired = session.get('token_info').get('expires_at') - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid

def get_tracks(sp):
    results = []
    iter = 0

    while True:
        offset = iter * 50
        iter += 1
        curGroup = sp.current_user_saved_tracks(limit=50, offset=offset)['items']
        for idx, item in enumerate(curGroup):
            track = item['track']
            val = track['name'] + " - " + track['artists'][0]['name']
            results += [val]
        if (len(curGroup) < 50):
            break
    #save_songs_csv(results, "Data/songs.csv")
    return results

def save_songs_csv(list, path):
    try:
        with open(path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            #songs = {line[0] for line in reader if line}

            if os.path.getsize(path) == 0:
                writer.writerow(["Song Name - Author"])
            writer.writerows([[song] for song in list if song not in path])

    except FileNotFoundError:
        songs = set()


