# mdg is tool to render a mididings script
### mididings is required
* https://github.com/mididings/mididings
### It creates a mididings script from a collection of files defined by YOU.
* The configuration files are src/config.json and main.mako template
* asoundrc.mako is optional and is the template for audio device
  * Because ALSA ports assignation for PCM is dynamic the builder take care of this:
    * Configure an ~/.asoundrc for audio devices with the help of pyalsaaudio

## How it works
* Entry point is /src/app.py and loads the configuration file
  * Then, it render to stdout a mididings script by replacing tokens in all Mako templates
## Includes
  * The src/includes contains files that will create the main body of the mididings script. The order of the files is important and it's defined in config.json.
## Extensions
  * The scr/extensions directory contains callable objects
    * Those extensions allow my mididings configuration to control modules I need like :
      * mpv - in JSON IPC mode to play audio files
        * It can start an instance of mpv for each sound card, each instance of mpv can play multiple audio files in parallel, this is possible with an asoundrc configuration that sets my PCM devices as dmix type
      * Philips Hue - API allow the send requests to a Philips Hue Bridge
      * Spotify - call their API to control a player
      * AKAI MIDIMIX - Helper to manage the switch state and the LED of the Akai MIDIMIX
## Dependencies
* Mako
## Optionals dependencies
* mpv
* pyliblo3 
* pyinotify
* pyalsaaudio
* spotipy
* phue
