# -*- coding: utf-8 -*-
from flask import request, jsonify
import math
import csv
from dotenv import load_dotenv
from API import *

load_dotenv()

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

