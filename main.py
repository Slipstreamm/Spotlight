from nicegui import ui, app, events
import json, spotifyapi
from pprint import pprint
green = '#3f9421'

with ui.header(elevated=True).style('background-color: #3f9421').classes('items-center justify-center'):
    ui.link('Spotlight', '/').style('font-size: 135%; text-decoration: none; color: #FFFFFF')
    ui.link('Top Tracks', '/tracks').style('color: #FFFFFF').style('font-size: 110%; text-decoration: none')
    ui.link('Top Artists', '/artists').style('color: #FFFFFF').style('font-size: 110%; text-decoration: none')
    ui.link('Top Genres', '/tracks').style('color: #FFFFFF').style('font-size: 110%; text-decoration: none')
    ui.link('Recent Streams', '/recent').style('color: #FFFFFF').style('font-size: 110%; text-decoration: none')
    ui.button('Login with Spotify', on_click=lambda: spotifyapi.authorizeApp()).props('color=black')
    ui.button('Full Reload', on_click=lambda: homepage.refresh()).props('color=black').classes(replace='items-center justify-right')

@ui.refreshable
def homepage():
    def appInfoExists():
        if(app.storage.general['id'] == ""):
            return False

    if(appInfoExists() == False):
        def saveDetails(id, secret):
            app.storage.general['id'] = id
            app.storage.general['secret'] = secret
            ui.notify('Info saved, you may close the dialog')

        with ui.dialog(value=True) as d, ui.card():
            ui.label('Create an app at https://developer.spotify.com/dashboard and enter it\'s details here. They will be stored locally in plaintext.')
            ui.label('http://127.0.0.1:1337/callback must be set as a redirect URI in your app.')
            with ui.row():
                t1 = ui.input(label='ID', placeholder='Your client id')
                t2 = ui.input(label='Secret', placeholder='Your client secret')
                ui.button('Save', on_click=lambda: saveDetails(t1.value, t2.value))

    if(app.storage.general['loggedin'] == 0):
        with ui.column(align_items='center') as c:
            c.classes('justify-center items-start mx-auto')
            c.style('padding-top: 50px')
            #ui.image(source='https://placehold.co/200x200').props('fit=scale-down').style('width: 200px; height: 200px;')
            ui.label('Login to start using Spotlight').style('font-size: 150%')

    if(app.storage.general['loggedin'] == 1):
        p = spotifyapi.getProfile(app.storage.general['accesstoken'])   
        with ui.column(align_items='center') as c:
            c.classes('justify-center items-start mx-auto')
            c.style('padding-top: 30px')
            ui.label('Your Profile').style('font-size: 150%')
            ui.image(source=p['images'][1]['url']).props('fit=scale-down').style('width: 200px; height: 200px;')
            with ui.row():
                ui.label(p['display_name']).style('font-size: 120%')
                ui.label(p['product']).style('font-size: 120%').props('color=orange')

homepage()

@ui.page(path='/callback', title='Spotlight', favicon='✅')
def callback(code: str = None):
    if(code != None):
        ui.label('Authorization successful. You may now close this tab.').classes('justify-center items-center mx-auto')
        app.storage.general['code'] = code
        app.storage.general['loggedin'] = 1
        spotifyapi.newToken()
        homepage.refresh()

@ui.refreshable
@ui.page(path='/tracks', title='Top Tracks - Spotlight')
def tracks():
    with ui.header(elevated=True).style('background-color: #3f9421').classes('items-center justify-center'):
        ui.link('Spotlight', '/').style('font-size: 135%; text-decoration: none; color: #FFFFFF')
        ui.link('Top Tracks', '/tracks').style('color: #FFFFFF').style('font-size: 110%; text-decoration: none')
        ui.link('Top Artists', '/artists').style('color: #FFFFFF').style('font-size: 110%; text-decoration: none')
        ui.link('Top Genres', '/tracks').style('color: #FFFFFF').style('font-size: 110%; text-decoration: none')
        ui.link('Recent Streams', '/recent').style('color: #FFFFFF').style('font-size: 110%; text-decoration: none')
        ui.button('Login with Spotify', on_click=lambda: spotifyapi.authorizeApp()).props('color=black')
        ui.button('Full Reload', on_click=lambda: tracks.refresh()).props('color=black').classes(replace='items-center justify-right')
    t = spotifyapi.topItems(50, 'tracks', 'long_term', app.storage.general['accesstoken'])
    with ui.list() as l:
        l.classes('justify-center items-start mx-auto')
        i=0
        a=0
        for item in t['items']:
            i=i+1
            a=0
            with ui.row():
                ui.label(f'#{i}').style('font-size: 120%; padding-top: 22px')
                ui.image(source=item['album']['images'][0]['url']).props('fit=scale-down').style('width: 70px; height: 70px;')
                ui.label.default_style('font-size: 120%; padding-top: 22px')
                ui.label(f'{item['name']}')
                ui.space()
                for artist in item['artists']:
                    a=a+1
                    artists = len(item['artists'])
                    #print(artists)
                    if(artists > 1):
                        if(a == artists):
                            ui.label(f'{artist['name']}')
                        else:
                            ui.label(f'{artist['name']},')
                    elif(artists == 1):
                        ui.label(f'{artist['name']}')
                with ui.link(target=f'{item["external_urls"]['spotify']}').style('padding-top: 20px; height: 30px; width: 30px;') as s:
                    s.classes('w-32 h-32')
                    ui.image('images/spotifywhite.png').props('fit=scale-down').style('width: 30px; height: 30px; padding-top: 20px')
                    ui.tooltip('Open on Spotify')
                with ui.link(target='/track').style('padding-top: 20px; height: 30px; width: 30px;') as s:
                    s.classes('w-32 h-32')
                    ui.image('images/spotifywhite.png').props('fit=scale-down').style('width: 30px; height: 30px; padding-top: 20px')
                    ui.tooltip('Open on Spotify')
            with ui.column():
                ui.space()
                ui.separator()
                ui.space()

ui.run(host='127.0.0.1', port=1337, native=False, favicon='🔦', title='Spotlight', dark=True, storage_secret='123')