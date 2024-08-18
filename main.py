from nicegui import ui, app
import json, spotifyapi
from pprint import pprint
green = '#3f9421'

with ui.header(elevated=True).style('background-color: #3f9421').classes('items-center justify-center'):
    ui.link('Spotlight', '/home').style('font-size: 135%; text-decoration: none; color: #FFFFFF')
    ui.link('Top Tracks', '/tracks').style('color: #FFFFFF').style('font-size: 110%; text-decoration: none')
    ui.link('Top Artists', '/artists').style('color: #FFFFFF').style('font-size: 110%; text-decoration: none')
    ui.link('Top Genres', '/tracks').style('color: #FFFFFF').style('font-size: 110%; text-decoration: none')
    ui.link('Recent Streams', '/recent').style('color: #FFFFFF').style('font-size: 110%; text-decoration: none')
    ui.button('Login with Spotify', on_click=lambda: spotifyapi.authorizeApp()).props('color=black')

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
            c.style('padding-top: 50px')
            ui.image(source=p['images'][1]['url']).props('fit=scale-down').style('width: 200px; height: 200px;')
            ui.label(p['display_name']).style('font-size: 120%')

homepage()

@ui.page(path='/callback', title='Spotlight', favicon='✅')
def callback(code: str = None):
    if(code != None):
        ui.label('Authorization successful. You may now close this tab.').classes('justify-center items-center mx-auto')
        app.storage.general['code'] = code
        app.storage.general['loggedin'] = 1
        spotifyapi.newToken()
        homepage.refresh()
        
ui.run(host='127.0.0.1', port=1337, native=False, favicon='🔦', title='Spotify Stats', dark=True, storage_secret='123')