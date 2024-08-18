import requests, base64, json
from pprint import pprint
from http.server import BaseHTTPRequestHandler, HTTPServer
from nicegui import ui, app

def authorizeApp():
    redirecturi = 'http://127.0.0.1:1337/callback'
    scope = 'user-read-private user-read-recently-played user-top-read user-follow-read user-library-read playlist-read-private playlist-read-collaborative user-read-currently-playing user-read-playback-state'
    id = app.storage.general['id']
    ui.navigate.to(f'https://accounts.spotify.com/authorize?response_type=code&client_id={id}&scope={scope}&redirect_uri={redirecturi}', new_tab=True)

def newToken():
    id = app.storage.general['id']
    secret = app.storage.general['secret']
    code = app.storage.general['code']
    redirecturi = 'http://127.0.0.1:1337/callback'
    authstring = f'{id}:{secret}'
    authstring = authstring.encode('utf-8')
    auth = base64.b64encode(authstring)
    auth = auth.decode('utf-8')
    with requests.post('https://accounts.spotify.com/api/token', {'code': code, 'redirect_uri': redirecturi, 'grant_type': 'authorization_code'}, headers={'content-type': 'application/x-www-form-urlencoded', 'Authorization': f'Basic {auth}'}) as r:
        res = r.content.decode('utf-8')
        res = json.loads(res)
        app.storage.general['accesstoken'] = res['access_token']
        app.storage.general['tokentype'] = res['token_type']
        app.storage.general['scope'] = res['scope']
        app.storage.general['expiresin'] = res['expires_in']
        app.storage.general['refreshtoken'] = res['refresh_token']

def refreshToken():
    None

def getProfile(key: str):
    with requests.get(f'https://api.spotify.com/v1/me', headers={'Authorization': f'Bearer {key}'}) as r:
        res = json.loads(r.text)
        return res

def topItems(x: int, type: str, range: str, key: str):
    with requests.get(f'https://api.spotify.com/v1/me/top/{type}?limit={x}&time_range={range}', headers={'Authorization': f'Bearer {key}'}) as r: 
        res = json.loads(r.text)
        return res