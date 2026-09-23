
'''
Patches to control somes /extensions/ modules
Those modules are callable objects (__call__)
'''

terminal = TerminalUI()
manager = PlaylistManager(terminal)

# MPV adapters for audio and video devices, using the socket paths from the config
mpv_config = config.get("mpv").get("socket")
AUDIO_DEVICE_SD90_A = Call(MpvAdapter(mpv_config.get("SD90_A"), manager.playlist, terminal))
AUDIO_DEVICE_SD90_B = Call(MpvAdapter(mpv_config.get("SD90_B"), manager.playlist, terminal))
AUDIO_DEVICE_SD90_VIDEO  = Call(MpvAdapter(mpv_config.get("SD90_VIDEO"), manager.playlist, terminal))

AUDIO_DEVICE_U192k_A  = Call(MpvAdapter(mpv_config.get("U192k_A"), manager.playlist, terminal))
AUDIO_DEVICE_U192k_B  = Call(MpvAdapter(mpv_config.get("U192k_B"), manager.playlist, terminal))
AUDIO_DEVICE_U192k_VIDEO  = Call(MpvAdapter(mpv_config.get("U192k_VIDEO"), manager.playlist, terminal))

MPV_VIDEO = Call(MpvAdapter(mpv_config.get("VIDEO"), manager.playlist, terminal))

# Playlist according to current scene, a singleton is enough
PLAYLIST_MANAGER = Call(manager)

terminal.start()
