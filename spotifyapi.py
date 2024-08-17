import requests

def topItems(x, type, range, key):
    with requests.get(f'https://api.spotify.com/v1/me/top/{type}?limit=50&time_range={range}') as r:
        r.headers = f'Authorization: Bearer {key}'
        return r