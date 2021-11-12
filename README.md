# Donoduck
Simple and free text-to-speech client for live streamers powered by Uberduck.


-----------------------------


Go to the releases tab on the right, download the latest "donoduck.zip" from the assets list, and unzip it. You can right click the executable and make a shortcut if you want to put it on your desktop or whatever. Just don't move the executable itself from the folder. Ducks get mad when you take them from their pond.

Donors can choose which voice their message will play with by putting "!voicenamehere: " at the beginning of their message.

"Voices.txt" contains the list of voices the program will default to at random if a voice isn't chosen. If the voice file is deleted or moved, the program will automatically generate a new one containing all 1400+ options. The full list of possible voices can be found here or in the duckvoices.py file. 

    https://uberduck.ai/quack-help
    
"Token.txt" is your socket token that will get incoming data from Streamlabs. Later this week this will be done in one click with an oauth link but for now you click this link, register an app, and get "Your Socket API Token" from the API Tokens tab. Just make sure it has permissions to access donations.

    https://streamlabs.com/dashboard#/settings/api-settings
    
Once these two files have stuff in then just run the executable let it sit in the background while you stream so that it may scream in the funny voices of your choosing whenever you convince someone to give you money.
