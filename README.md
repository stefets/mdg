# mdg is tool to build a mididings script
Creates a mididings script from a configuration file (src/config.json) and Mako templates

# How it works
* Use the mididings community version.
* app.mako is the template of the script
* asoundrc.mako is the template for audio device
  * Because ALSA ports assignation for PCM is dynamic the builder take care of this:
    * Configure an ~/.asoundrc for audio devices with the help of pyalsaaudio
* Entry point is /src/app.py and loads the configuration file
  * Then, it render to stdout a mididings script by replacing tokens in all Mako templates
# Includes
  * The src/includes contains files that will create the main body of the mididings script. The order of the files is important and it's defined in config.json.
# Extensions
  * The scr/extensions directory contains callable objects
    * Those extensions allow my mididings configuration to control modules I need like :
      * mpg123 - in remote mode to play MP3 audio files
        * It can start an instance of mpg123 for each sound card, each instance of mpg123 can play multiple audio files in parallel, this is possible with an asoundrc configuration that sets my PCM devices as dmix type
      * Philips Hue - API allow the send requests to a Philips Hue Bridge
      * Spotify - call their API to control a player
      * Request - send HTTP requests to any API
      * VLC Server - Send HTTP requests to a VLC server
      * AKAI MIDIMIX - Helper to manage the switch state and the LED of the Akai MIDIMIX
# Dependencies
* mididings, pyliblo3, pyinotify
* vlc and python-vlc-http
* mpg123 (recommended) or mpyg321 (not recommended)
* python-dotenv
* pyalsaaudio
* colorama
* requests
* spotipy
* Mako
* phue
* argh
# mididings
* https://github.com/mididings/mididings (maintained)
