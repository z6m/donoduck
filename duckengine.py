import multiprocessing
import os
import playsound
import random
import requests
import time
import tokens
import colorama
from colorama import Fore, Style
from colorama.ansi import Back
from pynput import keyboard

duck_token = tokens.duck_token
duck_secret = tokens.duck_secret
twitch_chat_token = tokens.twitch_chat_token
twitch_client_id = tokens.twitch_client_id
token_file = 'token.txt'
voice_file = 'voices.txt'
config_file = 'user_config.txt'
queue = 0

def get_endpoint(uuid):
        path = None
        while (path == None):
            r = requests.get('https://api.uberduck.ai/speak-status?uuid=' + uuid, auth=('$duck_token', '$duck_secret'))
            path = r.json()['path']
        return path 

def get_uuid(message, voice):
    # Send uberduck our text and the voice we want
    data = '{"speech":"%s.","voice":"%s"}' % (message, voice)
    r = requests.post('https://api.uberduck.ai/speak', data=data, auth=(duck_token, duck_secret))
    uuid = r.json()['uuid']
    return uuid

def get_audio(endpoint):
    global queue
    r = requests.get(endpoint)
    while queue >= 1:
        # Stops audio from trying to save over/overlap eachother shades: :v captain-falc
        time.sleep(1)
    queue = queue + 1
    audio_file = 'tts.wav'
    open(audio_file , 'wb').write(r.content)
    return audio_file

def cleanup(fname):
    os.remove(fname)
    
def get_voice():
    voices_list = open(voice_file).read().split()
    voice = random.choice(voices_list)
    return voice

def get_color(type):
    match type:
        case 'donation':
            color = Back.GREEN + Style.BRIGHT
        case 'bits':
            color = Back.CYAN + Style.BRIGHT
        case 'subscription':
            color = Back.MAGENTA + Style.BRIGHT
        case 'resub':
            color = Back.MAGENTA + Style.BRIGHT
        case 'chat':
            color = Fore.WHITE
    return color

def play(audio, skip_key):
    # Play message in different process so playsound will let go of the file when it's done
    playing = multiprocessing.Process(target=playsound.playsound, args=(audio,), kwargs={"block" : True})
    playing.start()

    def emergency_skip(key):
        # [8:27 PM] Doc: Lol this exact bit of code was duplicated about 3 dozen times in the repo of the company i used to be at
        def my_import(name):
            components = name.split('.')
            mod = __import__(components[0])
            for comp in components[1:]:
                mod = getattr(mod, comp)
            return mod

        if key == my_import("pynput.keyboard.Key." + skip_key):
            playing.terminate()

    # Skip button in case voice freaks out
    skipping = keyboard.Listener(on_press=emergency_skip)
    skipping.start()

    playing.join()

    global queue
    queue = 0

def listen():
    print(Fore.YELLOW + '[*] The duck is listening...')