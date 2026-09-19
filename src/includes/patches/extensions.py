
'''
Patches to control somes /extensions/ modules
Those modules are callable objects (__call__)
'''

terminal = TerminalUI()
manager = PlaylistManager(terminal)

# AUDIO_DEVICE multiple instances allow me to play sounds in parallal (dmix)
mpv_config = config.get("mpv").get("socket")
AUDIO_DEVICE_SD90_A = Call(MpvAdapter(mpv_config.get("SD90_A"), manager.playlist, terminal))
AUDIO_DEVICE_SD90_B = Call(MpvAdapter(mpv_config.get("SD90_B"), manager.playlist, terminal))
AUDIO_DEVICE_U192k  = Call(MpvAdapter(mpv_config.get("U192k"), manager.playlist, terminal))

# Playlist according to current scene, a singleton is enough
PLAYLIST_MANAGER = Call(manager)

terminal.start()
