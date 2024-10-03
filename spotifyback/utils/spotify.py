# -*- coding: utf-8 -*-
from flask import url_for, request, jsonify, session
from spotipy.oauth2 import SpotifyOAuth
import time
import math
import csv
import os

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
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

def get_tracks(sp, path):
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

    save_songs_csv(results, path)
    return results

def save_songs_csv(list, path):
    try:
        with open(path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows([[song] for song in list if song not in path])

    except FileNotFoundError:
        songs = set()


def read_csv(all_tracks, path):
    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)

        for row in csvreader:
            all_tracks.append(row)
    return all_tracks

def pagination(all_tracks):
    ITEMS_PER_PAGE = 50
    page = int(request.args.get('page', 1))
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    if isinstance(all_tracks, list):
        tracks_on_page = all_tracks[start:end]
        total_pages = math.ceil(len(all_tracks) / ITEMS_PER_PAGE)
        return jsonify({
            "tracks": tracks_on_page,
            "total_pages": total_pages,
            "current_page": page
        })
    else:
        return jsonify({"error": "Error fetching tracks, data is not a list"}), 500

def tracks(path, sp):
    if not os.path.exists(path) or os.stat(path).st_size == 0:
        tracks = get_tracks(sp, path)
        return tracks
    else:
        tracks = []
        tracks = read_csv(tracks, path)
        return tracks
