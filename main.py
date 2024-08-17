from nicegui import ui
import json
from spotifyapi import *
green = '#3f9421'

def appInfoExists():
    try:
        with open('settings.json') as f:
            data = json.load(f)
            return 'id' in data
    except json.JSONDecodeError:
        print('Error decoding JSON.')
        return False
    
    
if(appInfoExists() == False):
    def saveDetails(id, secret):
        with open('settings.json', mode='w') as f:
            data = {'id': id, 'secret': secret}
            json.dump(data, f)
            ui.notify('Saved. You may close the dialog.')

    with ui.dialog(value=True) as d, ui.card():
        ui.label('Create an app at https://developer.spotify.com/dashboard and enter it\'s details here. They will be stored locally in plaintext.')
        with ui.row():
            t1 = ui.input(label='ID', placeholder='Your client id')
            t2 = ui.input(label='Secret', placeholder='Your client secret')
            ui.button('Save', on_click=lambda: saveDetails(t1.value, t2.value))

with ui.header(elevated=True).style('background-color: #3f9421').classes('items-center justify-center'):
    ui.label('Spotify Stats').style('font-size: 110%')
    ui.link('Top Tracks', '/tracks').style('color: #FFFFFF').style('font-size: 110%')
    ui.link('Top Artists', '/artists').style('color: #FFFFFF').style('font-size: 110%')
    ui.link('Top Genres', '/tracks').style('color: #FFFFFF').style('font-size: 110%')
    ui.link('Recent Streams', '/recent').style('color: #FFFFFF').style('font-size: 110%')

with ui.column(align_items='center') as c:
    c.classes('justify-center items-start mx-auto')
    c.style('padding-top: 50px')
    ui.image(source='https://placehold.co/200x200').props('fit=scale-down').style('width: 200px; height: 200px;')
    ui.label('Your Username Here').style('font-size: 110%')

ui.run(host='127.0.0.1', port=1337, native=False, favicon='📊', title='Spotify Stats', dark=True)