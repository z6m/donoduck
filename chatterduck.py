import configparser
import duckengine
import duckvoices
import multiprocessing
import os
import pyfiglet
import re
import colorama
from colorama import Fore, Style
from colorama.ansi import Back
from twitchio.ext import commands

if __name__ == '__main__':
    multiprocessing.freeze_support() # This makes multiprocessing work
    colorama.init(autoreset=True)

    # Set duck_cfg as working directory
    if os.path.isdir('duck_cfg') == False and os.getcwd != 'duck_cfg':
        os.mkdir('duck_cfg')
    os.chdir("duck_cfg")

    for item in os.listdir('./'):
            if item.endswith(".wav"):
                duckengine.cleanup(item)

    # Version info
    version_name = "I Have No Idea What I'm Doing Edition"
    version_tag = 'v0.2'
    channel_name = 'zoms'

    # Read config file
    config = configparser.ConfigParser()
    config.read(duckengine.config_file)
    print(duckengine.config_file)

    # Check for voice file
    if os.path.isfile(duckengine.voice_file) == False:
        open(duckengine.voice_file, "w+")
        print ("[*] Voice list generated")

    # Check for populated voice file
    if os.stat(duckengine.voice_file).st_size == 0:
        print("[*] Voice file empty \n[*] Populating voice file")
        # If there are no voices in the file we will put them there ourselves
        f = open(duckengine.voice_file, "w+")
        for voice in duckvoices.voices():
            f.writelines(voice + "\n")
        f.close()

    # Header
    header = pyfiglet.figlet_format('Chatterduck', font='chunky')
    print(Fore.YELLOW + header + '[' + version_name + '] ' + version_tag + "\n \n"
        "(*)< Full voice list // " + Fore.WHITE + "https://github.com/z6m/donoduck/blob/main/duckvoices.py \n" + Fore.YELLOW +
        "(*)< Choose voice with message // " + Fore.WHITE + '"!tts voice-goes-here: message-goes-here" \n' + Fore.YELLOW +
        "(*)< Press " + config['Settings']['skip_key'] + " to skip message \n")

    # Run
    def run(message, type):
        # Slice up voice from message
        if message.startswith('!') == True and ':' in message:
            message = re.search('!(\S*):(.*)', message)
            voice = message.group(1)
            voice = voice.lower()
            message = message.group(2)
            if voice not in duckvoices.voices:
                voice = duckengine.get_voice()
                print(Fore.RED + "[X] Getting random voice")
        else: 
            voice = duckengine.get_voice()
            message = " " + message 

        # This fixes an occasional api error
        try:
            uuid = duckengine.get_uuid(message, voice) # this is problem
        except:
            run(message, type) 
            print(Fore.RED + "[!] Failed at uuid")
            return

        # Get the rest of our stuff
        try:
            endpoint = duckengine.get_endpoint(uuid)
        except:
            print (Fore.RED + "Failed to get endpoint")
        fname = duckengine.get_audio(endpoint)
        # Trying to keep audio files from playing at once

        print('(*)< ' + Fore.WHITE + voice + ":" + message)
        try:    
            duckengine.play(fname, config['Settings']['skip_key'])
        except:
            print (Fore.RED + "[!] Failed to get endpoint")

        # Clean up your mess
        duckengine.cleanup(fname)
        return

    # BOT STUFF STARTS HERE
    bot = commands.Bot(
        token=duckengine.twitch_chat_token,
        client_id=duckengine.twitch_client_id,
        nick="chatterduck",
        prefix=";",
        initial_channels=[channel_name],
    )

    @bot.event
    async def event_message(msg):
        msg = msg.message.content.lower()
        await bot.handle_commands(msg)

    @bot.command(name='v')
    async def test_cmd(msg):
        message = msg.message.content
        message = message.replace(';v ', '!').strip()
        print (Fore.BLACK + Style.BRIGHT + "[*]" + message)
        if message != "!":
            run(message,type='chat')

    bot.run()