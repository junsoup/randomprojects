from flask import Flask, redirect, request, session, url_for
from cover_image import ImageProcessor
import requests
import time
import threading
import random
import string
import json

app = Flask(__name__)
app.secret_key = 'some_secret_key'  # Replace with a real secret key

client_id = 'put_in_your_key_i_removed_mine'
client_secret = 'this_one_too'
redirect_uri = 'http://localhost:3000/callback'
scope = 'user-read-playback-state'
# Global variables to store access token details
access_token = None
refresh_token = None
token_expires_in = None
token_obtained_at = None

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

@app.route('/login')
def login():
    state = generate_random_string(16)
    session['state'] = state
    auth_url = (
        'https://accounts.spotify.com/authorize'
        '?response_type=code'
        '&client_id={}'
        '&scope={}'
        '&redirect_uri={}'
        '&state={}').format(client_id, scope, redirect_uri, state)
    return redirect(auth_url)

@app.route('/callback')
def callback():
    global access_token, refresh_token, token_expires_in, token_obtained_at

    code = request.args.get('code')
    state = request.args.get('state')
    if state != session['state']:
        return 'State mismatch!', 400

    token_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(token_url, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    })

    response_data = response.json()
    access_token = response_data['access_token']
    refresh_token = response_data['refresh_token']
    token_expires_in = response_data['expires_in']
    token_obtained_at = time.time()
    start_polling_thread()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return 'Logged in. Polling for currently playing track has started.'

def get_currently_playing(access_token):
    url = 'https://api.spotify.com/v1/me/player/currently-playing'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and response.json():
        data = response.json()
        item = data['item']
        track_id = item['id']
        track_name = item['name']
        artist_name = item['artists'][0]['name']
        return track_id, track_name, artist_name
    return None, None, None

def get_track_image(track_id, access_token):
    url = f'https://api.spotify.com/v1/tracks/{track_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        track_data = response.json()
        album_data = track_data['album']
        # Assuming we want the first image (largest size) for simplicity
        if 'images' in album_data and album_data['images']:
            image_url = album_data['images'][0]['url']
            return image_url
    return None

def refresh_access_token():
    global access_token, refresh_token, token_expires_in, token_obtained_at

    token_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(token_url, data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    })

    response_data = response.json()
    access_token = response_data['access_token']
    if 'refresh_token' in response_data:
        refresh_token = response_data['refresh_token']
    token_expires_in = response_data['expires_in']
    token_obtained_at = time.time()

def poll_for_changes():
    global access_token, token_expires_in, token_obtained_at

    previous_track_id = None
    while True:
        # Check if the token is expired or about to expire in 1 minute
        if time.time() > token_obtained_at + token_expires_in - 60:
            refresh_access_token()

        if access_token:
            track_id, track_name, artist_name = get_currently_playing(access_token)
            if track_id and track_id != previous_track_id:
                art = get_track_image(track_id, access_token)
                processed_string = ''
                image = ImageProcessor.download_image(art)
                if image:
                    resized_grayscale_image = ImageProcessor.resize_and_grayscale_image(image)
                    if resized_grayscale_image:
                        # Process the grayscale image to map pixel values to 0-5 and get the concatenated string
                        processed_string = ImageProcessor.process_grayscale_image(resized_grayscale_image)
                        if not processed_string:
                            print("Failed to process grayscale image.")
                    else:
                        print("Failed to resize and convert image to grayscale.")
                else:
                    print("Failed to download image.")
                
                # Use lcu to fill these given league instance
                previous_track_id = track_id
                ip = 'https://127.0.0.1:53840/lol-chat/v1/me'
                headers = {'accept': 'application/json',
                        'Authorization': 'Basic cmlvdDpSSjBwNTRIenFUd0hyOWtsUFdGOTlB',
                        'Content-Type': 'application/json'
                }
                space = '　'
                out = {"statusMessage": f"Now playing...{space*20}\n {track_name} by {artist_name} {space*30}\n {processed_string}"}
                data = json.dumps(out, ensure_ascii=False).encode('utf-8')
                response = requests.put(ip, verify=False, headers=headers, data=data)
                # Invoke your callback here
                print(processed_string)
                print(f'Now playing: {track_name} by {artist_name}, image url {art}')
        time.sleep(10)  # Poll every 10 seconds

# Start polling in a separate thread after the user logs in
def start_polling_thread():
    polling_thread = threading.Thread(target=poll_for_changes)
    polling_thread.daemon = True
    polling_thread.start()

if __name__ == '__main__':
    app.run(port=3000)
    
