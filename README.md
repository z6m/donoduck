<p align="center">
    <img width="250" src="https://user-images.githubusercontent.com/58152411/169162076-17c98ab8-d4e4-429f-8fc9-7e89b5f96342.png" alt="Duck lol">
</p>

# Donoduck
Simple and free custom text-to-speech client for live streamers with over 2200 voices ~~that I'm stealing from~~ <em>powered by</em> [Uberduck](https://uberduck.ai/).

    
    
# Setup Guide
Go to the [releases](https://github.com/z6m/donoduck/releases) page, download the latest "Donoduck.zip" from the assets list, and unzip it. You can make a shortcut if you want to put it on your desktop or whatever.

Run the executable and let it sit in the background while you stream so that it may scream in the funny voices of your choosing whenever you convince someone to give you money. Chatters can choose which voice their message will play with by formatting their message like this:

    "!voice-name-here: message text here" 

(NOTE: ff you have some other TTS thing turn it off or they'll both play at once)
(ALSO NOTE: If there's a delay between alerts popping up and messages being played you can compensate for it by setting the [alert delay](https://streamlabs.com/dashboard#/alertbox) to like 2-5 seconds. Can't do much about that on my end for now.)

# duck_cfg
token.txt 
> is your socket token that will get incoming data from Streamlabs/Streamelements. Get that here:

    https://streamlabs.com/dashboard#/settings/api-settings

voices.txt
> contains the voice(s) the program will default to if a voice isn't chosen (will pick at random if list contains multiple entries). Some voices are way better than others, you will probably want to customize this. The full list of supported voices can be found in duckvoices.py:

    https://github.com/z6m/donoduck/blob/main/duckvoices.py

user_config.txt
> contains everything else.
>
> "skip_key" is the hotkey that you can use to skip donations if voices glitch out or whatever. By default it's set to RIGHT SHIFT since it's the most useless key I can think of that most keyboards have and won't mess anything up in most programs. You can find all the aliases for the different keys here if you want to change it:
        
    https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key

> "min_bits" is the minumum number of bits someone has to tip to play tts. This is just to avoid spam. It's 100 by default.

# Nightbot Command
Really easy copypaste rundown for lazy people (like me) to add as a command to nightbot:

    !addcom !tts Donoduck is a free text-to-speech client with over 2200 voices. To have your message read in a custom voice, put !name-of-voice: at the start of your message. Full list of voices here: https://github.com/z6m/donoduck/blob/main/duckvoices.py
       


# Compiling from source 
If you're into that kinda thing (path to pyfiglet may vary and you'll need to get your own uberduck api tokens):

    pyinstaller --add-data "C:\Users\*****\AppData\Local\Programs\Python\Python310\Scripts;./pyfiglet" -i "logo.ico" -n Donoduck --onefile donoduck.py

-----------------------------------------------------------

OTHER NOTE: Right now I'm totally freeloading so there could be several seconds of lag between some alerts and them being read out. If people actually start using this I'll shell out so you can get that sweet unthrottled api access on my dime (or you can compile yourself/hit me up on twitter and I'll make you a custom build with your own premium keys if you got 'em).
