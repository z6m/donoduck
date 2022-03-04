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

if __name__ == '__main__':
    multiprocessing.freeze_support()
    colorama.init()

    version_name = 'Streamlabs Beta Edition'
    version_tag = 'v1'

    s = socketio.Client()
    token_file = 'token.txt'
    voice_file = 'voices.txt'
    queue = 0

    # Header
    header = pyfiglet.figlet_format('Donoduck', font='chunky')
    print(Fore.YELLOW + header + '[' + version_name + '] ' + version_tag + "\n \n"
        "(*)< Full voice list // " + Fore.WHITE + "https://github.com/z6m/donoduck/blob/main/duckvoices.py \n" + Fore.YELLOW +
        "(*)< For custom voices // " + Fore.WHITE + "!voice-goes-here: message-goes-here \n" + Fore.RESET)

    # Check Version
    try:
        response = requests.get("https://api.github.com/repos/z6m/donoduck/releases/latest")
        latest_version = response.json()["tag_name"]
        if latest_version != version_tag:
            print(Fore.RED + Style.BRIGHT + "(*)< A new version of Donoduck is out\n"
                "(*)< Download it here: " + Style.RESET_ALL + "https://github.com/z6m/Donoduck/releases/latest\n")
    except:
        print(Fore.RED + Style.BRIGHT + "(*)< Rate limit exceeded, skipping update check \n" + Style.RESET_ALL)

    if os.path.isfile(token_file) == False or os.stat(token_file).st_size == 0:
        f = open(token_file, "w+")
        f.writelines(input("[*] Paste your socket token here: "))
        f.close()
        print()
            
    sock_token = open(token_file, "r").read().strip()
    duck_token = tokens.duck_token
    duck_secret = tokens.duck_secret

    s.connect("https://sockets.streamlabs.com?token=%s" % (sock_token))

    def get_endpoint(uuid):
        # Poll the endpoint and grab the path to our audio
        path = None
        while (path == None):
            time.sleep(1)
            r = requests.get('https://api.uberduck.ai/speak-status?uuid=' + uuid, auth=('$duck_token', '$duck_secret'))
            path = r.json()['path']
        return path 

    def get_uuid(speech, voice):
        # Send uberduck our text and the voice we want
        data = '{"speech":"%s.","voice":"%s"}' % (speech, voice)
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

    def play(audio):
        # Play sound in different process so playsound will let go of the file when it's done
        job = multiprocessing.Process(target=playsound.playsound, args=(audio,), kwargs={"block" : True})
        job.start()
        job.join()
        global queue
        queue = 0

    def listen():
        print('[*] The duck is listening...')

    def run(message):
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

        # Get the rest of our stuff
        uuid = get_uuid(message, voice)
        endpoint = get_endpoint(uuid)
        fname = get_audio(endpoint)
         # Trying to keep audio files from playing at once
                    
        print('[!] ' + voice + ":" + message)
        play(fname)

        # Clean up your mess
        cleanup(fname)

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
        if event_data["type"] == "donation" or event_data["type"] == "bits" or event_data["type"] == "subscription" and event_data["message"][0]["message"] != None:
            print ("[$] Processing message from " + event_data["message"][0]["name"])
            run(event_data["message"][0]["message"])
            

    @s.on("disconnect")
    def disconnect():
        print("[*] He disgonegted yea guiys")

    s.wait()
