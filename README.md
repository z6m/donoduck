# Donoduck
Simple and free custom text-to-speech client for live streamers with over 1400 voices ~~that I'm stealing from~~ <em>powered by</em> [Uberduck](https://uberduck.ai/).


-----------------------------


Go to the releases tab, download the latest "Donoduck.zip" from the assets list, and unzip it. You can make a shortcut if you want to put it on your desktop or whatever.


"Token.txt" is your socket token that will get incoming data from Streamlabs/Streamelements. Get that here:

    https://streamlabs.com/dashboard#/settings/api-settings
    https://streamelements.com/dashboard/account/channels
    

"Voices.txt" contains the voice(s) the program will default to if a voice isn't chosen (will pick at random if list contains multiple entries). If no voice file exists in the current directory, the program will automatically generate a new one containing all 1400+ options. The full list of possible voices can be found in duckvoices.py:

    https://github.com/z6m/donoduck/blob/main/duckvoices.py

If you have some other TTS thing turn it off or they'll both play at once.


Run the executable and let it sit in the background while you stream so that it may scream in the funny voices of your choosing whenever you convince someone to give you money. 

    Tippers can choose which voice their message will play with by putting "!voice-name-here: message text here". 
    (NOTE: If you're having people cheer with bits, have them put the cheer stuff at the end of the message or it will mess this part up)

-----------------------------

# Nightbot 
Really easy copypaste rundown for lazy people (like me) to add as a command to nightbot:

       !addcom !tts Donoduck is a free text-to-speech client with over 1400 voices. To have your message read in a custom voice, put !name-of-voice: at the start of your message. Full list of voices here: https://github.com/z6m/donoduck/blob/main/duckvoices.py
       
-----------------------------

# Compiling from source 
If you're into that kinda thing (path to pyfiglet may vary):

       pyinstaller --add-data "C:\Users\*yourusernamehere*\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\site-packages\pyfiglet;./pyfiglet" -i "logo.ico" -n Donoduck --onefile donoduck.py

