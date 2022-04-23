import duckvoices
import multiprocessing
import os
import playsound
import pyfiglet
import random
import re
import requests
import socketio
import time
import tokens
import colorama
from colorama import Fore, Style
from colorama.ansi import Back
from pynput import keyboard

if __name__ == '__main__':
    multiprocessing.freeze_support()
    colorama.init(autoreset=True)

    # Version info
    version_name = 'Relatively Unscuffed Alpha Edition'
    version_tag = 'v1.1.1'

    # Files
    s = socketio.Client()
    token_file = 'token.txt'
    voice_file = 'voices.txt'
    skip_key = 'skip_key.txt'
    queue = 0
    if os.path.isdir('duck_cfg') == False:
        os.mkdir('duck_cfg')
    os.chdir("duck_cfg")

    # Default hotkey for skipping messages
    if os.path.isfile(skip_key) == False or os.stat(skip_key).st_size == 0:
        f = open(skip_key, "w+")
        f.writelines("shift_r")
        f.close()

    # Header
    header = pyfiglet.figlet_format('Donoduck', font='chunky')
    print(Fore.YELLOW + header + '[' + version_name + '] ' + version_tag + "\n \n"
        "(*)< Full voice list // " + Fore.WHITE + "https://github.com/z6m/donoduck/blob/main/duckvoices.py \n" + Fore.YELLOW +
        "(*)< Choose voice with message // " + Fore.WHITE + '"!voice-goes-here: message-goes-here" \n' + Fore.YELLOW +
        "(*)< Press " + open(skip_key, "r").read().strip().upper() + " to skip message \n")

    # Check version
    try:
        response = requests.get("https://api.github.com/repos/z6m/donoduck/releases/latest")
        latest_version = response.json()["tag_name"]
        if latest_version != version_tag:
            print(Fore.RED + Style.BRIGHT + "(*)< A new version of Donoduck is out\n"
                "(*)< Download it here: " + "https://github.com/z6m/Donoduck/releases/latest\n")
    except:
        print(Fore.RED + Style.BRIGHT + "(*)< Rate limit exceeded, skipping update check \n")

    # Input socket token
    if os.path.isfile(token_file) == False or os.stat(token_file).st_size == 0:
        f = open(token_file, "w+")
        f.writelines(input("[*] Paste your socket token here: "))
        f.close()
        print()

    # Tokens         
    sock_token = open(token_file, "r").read().strip()
    duck_token = tokens.duck_token
    duck_secret = tokens.duck_secret

    # Socket
    s.connect("https://sockets.streamlabs.com?token=%s" % (sock_token))

    def get_endpoint(uuid):
        path = None
        while (path == None):
            time.sleep(1)
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
            # Stops audio from trying to save over/overlap eachother
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
        return color

    def play(audio):
        # Play message in different process so playsound will let go of the file when it's done
        playing = multiprocessing.Process(target=playsound.playsound, args=(audio,), kwargs={"block" : True})
        playing.start()


        def emergency_skip(key):
            hotkey = open(skip_key, "r").read().strip()
            
            # [8:27 PM] Doc: Lol this exact bit of code was duplicated about 3 dozen times in the repo of the company i used to be at
            def my_import(name):
                components = name.split('.')
                mod = __import__(components[0])
                for comp in components[1:]:
                    mod = getattr(mod, comp)
                return mod

            if key == my_import("pynput.keyboard.Key." + hotkey):
                playing.terminate()

        # Skip button in case voice freaks out
        skipping = keyboard.Listener(on_press=emergency_skip)
        skipping.start()

        playing.join()

        global queue
        queue = 0

    def listen():
        print(Fore.YELLOW + '[*] The duck is listening...')

    def run(message, type):
        # Allow donator to pick voice
        if message.startswith('!') == True and ':' in message:
            message = re.search('!(.*):(.*)', message)
            voice = message.group(1)
            voice = voice.lower()
            message = message.group(2)
            if voice not in duckvoices.voices:
                voice = get_voice()
        else: 
            voice = get_voice()
            message = " " + message 

        # This fixes an occasional api error
        try:
            uuid = get_uuid(message, voice)
        except:
            run(message, type) 
            return

        # Get the rest of our stuff
        endpoint = get_endpoint(uuid)
        fname = get_audio(endpoint)
         # Trying to keep audio files from playing at once

        color = get_color(type)
                    
        print(color + '[!] ' + voice + ":" + message)
        play(fname)

        # Clean up your mess
        cleanup(fname)
        return

    @s.on("connect")
    def connect():
        # Remove leftover audio files
        for item in os.listdir('./'):
            if item.endswith(".wav"):
                cleanup(item)

        # Check for voice file
        if os.path.isfile(voice_file) == False:
            open(voice_file, "w+")
            print ("[*] Voice list generated")

        # Check for populated voice file
        if os.stat(voice_file).st_size == 0:
            print("[*] Voice file empty \n[*] Populating voice file")
            # If there are no voices in the file we will put them there ourselves
            f = open(voice_file, "w+")
            for voice in duckvoices.voices:
                f.writelines(voice + "\n")
            f.close()

        listen()

    @s.on("event")
    def event(event_data):
        if event_data["type"] == "donation" or event_data["type"] == "bits" or event_data["type"] == "subscription" or event_data["type"] == "resub" and event_data["message"][0]["message"] != None:
            print (Fore.BLACK + Style.BRIGHT + "[$] " + event_data["type"] + " from " + event_data["message"][0]["name"])
            run(event_data["message"][0]["message"], event_data["type"])
            

    @s.on("disconnect")
    def disconnect():
        print("[*] He disgonegted yea guiys")

    s.wait()
