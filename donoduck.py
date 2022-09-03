import configparser
import duckengine
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
    version_name = "Relatively Unscuffed Alpha Edition"
    version_tag = 'v1.1.2'

    # Files
    s = socketio.Client()
    token_file = 'token.txt'
    voice_file = 'voices.txt'
    config_file = 'user_config.txt'
    queue = 0
    
    # Config
    if os.path.isdir('duck_cfg') == False:
        os.mkdir('duck_cfg')
    os.chdir("duck_cfg")

    config = configparser.ConfigParser()
    config.read(config_file)

    # Header
    header = pyfiglet.figlet_format('Donoduck', font='chunky')
    print(Fore.YELLOW + header + '[' + version_name + '] ' + version_tag + "\n \n"
        "(*)< Full voice list // " + Fore.WHITE + "https://github.com/z6m/donoduck/blob/main/duckvoices.py \n" + Fore.YELLOW +
        "(*)< Choose voice with message // " + Fore.WHITE + '"!voice-goes-here: message-goes-here" \n' + Fore.YELLOW +
        "(*)< Press " + config['Settings']['skip_key'] + " to skip message \n")

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

    def run(message, type):
        # Allow donator to pick voice
        # Removes cheer message from string
        if message.startswith('cheer'):
                message = re.search('cheer(.\d*) (.*)', message)
                message = message.group(2)
        
        # Slice up voice from message
        if message.startswith('!') == True and ':' in message:
            message = re.search('!(\S*):(.*)', message)
            voice = message.group(1)
            voice = voice.lower()
            message = message.group(2)
            if voice not in duckvoices.voices:
                voice = duckengine.get_voice()
        else: 
            voice = duckengine.get_voice()
            message = " " + message 

        # This fixes an occasional api error
        try:
            uuid = duckengine.get_uuid(message, voice)
        except:
            run(message, type) 
            return

        # Get the rest of our stuff
        endpoint = duckengine.get_endpoint(uuid)
        fname = duckengine.get_audio(endpoint)
         # Trying to keep audio files from playing at once

        color = duckengine.get_color(type)
                    
        print(color + '[!] ' + voice + ":" + message)
        duckengine.play(fname, config['Settings']['skip_key'])

        # Clean up your mess
        duckengine.cleanup(fname)
        return

    @s.on("connect")
    def connect():
        # Remove leftover audio files
        for item in os.listdir('./'):
            if item.endswith(".wav"):
                duckengine.cleanup(item)

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

        duckengine.listen()

    @s.on("event")
    def event(event_data):
        if event_data["type"] == "bits":
            if int(event_data['message'][0]['amount']) < int(config['Settings']['min_bits']):                    
                return
        if event_data["type"] == "donation" or event_data["type"] == "bits" or event_data["type"] == "subscription" or event_data["type"] == "resub" and event_data["message"][0]["message"] != None:
            print (Fore.BLACK + Style.BRIGHT + "[$] " + event_data["type"] + " from " + event_data["message"][0]["name"])
            run(event_data["message"][0]["message"], event_data["type"])
            
        
    @s.on("disconnect")
    def disconnect():
        print("[*] He disgonegted yea guiys")

    s.wait()
