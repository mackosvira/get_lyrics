# API_lyrics_ovh.py
# lyrics.ovh API connector

import requests
import json
import re

API_URL = 'https://api.lyrics.ovh'

def fetch_suggestions(search_text, num_of_results=7):
    """
    connect to web site API for suggestions search
    returns list of suggestions in text form: "Title - Artist"
    in additin removes brackets text in "Title" fetched suggestions
    """

    # Clear previous results
    #self.menu.dismis()
    #print(search_text)

    # API request to fetch suggestions
    response = requests.get(f"{API_URL}/suggest/{search_text}")
    data = response.json()
    seen_results = []
    for result in data['data'][:num_of_results]:  # Limit to 7 results
        display_text = f"{re.sub(r"\s*\(.*?\)", "", result['title'])} - {result['artist']['name']}"
        #print(display_text)

        if display_text not in seen_results:
            seen_results.append(display_text)

    return seen_results


def get_lyrics(title,artist):
    """
    connect to web site API for lyric search using Title and Artist name
    returns distionary in form {"lyrucs":"lyrics text"}
    in case of no lyrics found, returns {"error":"lyrics not found"}
    """
    request=f"{API_URL}/v1/{artist}/{title}"
    response_body = requests.get(request)
    response = response_body.json()
    response= {key: value.replace("\n\n", "\r\n") for key, value in response.items()}
    return response


