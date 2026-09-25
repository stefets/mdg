
#
# Patches for the run().control patch
#

# Transport filters
jump_filter    = CtrlFilter(1)  >> CtrlValueFilter(0, 121)

# 0 = Mute is False / 127 = Mute is True
mute_filter    = CtrlFilter(2) >> [
    CtrlValueFilter(0),
    CtrlValueFilter(127)
]
volume_filter  = CtrlFilter(7)  >> CtrlValueFilter(0, 101)
transport_filter = [
    jump_filter,
    volume_filter, 
    Filter(NOTEON),
    mute_filter
]

mpv_controller_sd90_a = transport_filter >> AUDIO_DEVICE_SD90_A
mpv_controller_sd90_b = transport_filter >> AUDIO_DEVICE_SD90_B
mpv_controller_sd90_video = transport_filter >> AUDIO_DEVICE_SD90_VIDEO

mpv_controller_u192k_a = transport_filter >> AUDIO_DEVICE_U192k_A
mpv_controller_u192k_b = transport_filter >> AUDIO_DEVICE_U192k_B
mpv_controller_u192k_video = transport_filter >> AUDIO_DEVICE_U192k_VIDEO

mpv_controller_video = transport_filter >> MPV_VIDEO

sd90_controller = Port(sd90_port_a) >> [ 
    CtrlFilter(0) >> WaveLevel,
    CtrlFilter(1) >> InstLevel,
    CtrlFilter(2) >> MicGtLevel,
    CtrlFilter(3) >> DigiLevel,
    CtrlFilter(4) >> MasterLevel,
    CtrlFilter(5) >> RecLevel,
 ]

# Spotify
# spotify_controller = [
#   Filter(NOTEON),
#   volume_filter, 
#   CtrlFilter(44),
# ] >> Call(SpotifyPlayer())

soundcraft_controller=Filter(CTRL|NOTE) >> [
        Filter(CTRL) >> Pass(),
        Filter(NOTE) >> NoteOn(EVENT_NOTE, 127) >> Port(midimix_midi),
    ] >> soundcraft_control

# Common controller for MPK249 and MPK261
mpk_249_261_controller =  ChannelSplit({
         1 : CakewalkController,
         2 : mpv_controller_u192k_a,
         3 : mpv_controller_u192k_b,
         5 : mpv_controller_sd90_a,
         6 : mpv_controller_sd90_b,
        14: sd90_controller,
    })

# Midi input control patch
control_patch = PortSplit({

    # Akai MIDIMIX
    midimix_midi : soundcraft_control,

    # Akai MPK249 (DEVE/Backup)
    # Port A
    mpk249_port_a : Transpose(-36) >> mpk_249_261_controller,
    # Port B (WIP)
    mpk249_port_b : ChannelSplit({
        # Mapping of the MPK249 PADS BANK C
        1 : mpv_controller_video,
    }),  
    # DIN Port
    mpk249_midi : ChannelSplit({
        # Roland PK5 connected to the MIDI IN of the MPK249
        4 : Transpose(-36) >> mpv_controller_sd90_b,
    }),

    # Akai MPK261 (PROD)
    # Port A
    mpk261_port_a : Transpose(-24) >> mpk_249_261_controller,
    # Port B
    mpk261_port_b : ChannelSplit({
        # Mapping of the MPK261 PADS BANK C
        1 : mpv_controller_video,
        2: p_hue,
    }),
    # DIN Port
    mpk261_midi : ChannelSplit({
        # Roland PK5 connected to the MIDI IN of the MPK249
        4 : Transpose(-36) >> mpv_controller_sd90_b,
    }),
    
    # Direct routing of the Numark controllers to the virtual port used by Mixxx
    # This allow me to use other controllers in addition of the Numark controller to control Mixxx
    numark_midi_pmv3_0 : Port(mixxx_midi_0),
    numark_midi_pmv2_0 : Port(mixxx_midi_0),

    # Suspended for analysis, not used in the current configuration
    # mpk249_port_b : ChannelSplit({
    #      1 : Program(sd90_port_a, EVENT_CHANNEL, EVENT_VALUE),
    #      2 : Channel(1) >> Port(mixxx_midi_0),
    #      8 : mpv_controller_sd90_a,
    #      4 : mpv_controller_sd90_b,
    # }),
    # sd90_midi_1 : Pass(),
    # sd90_midi_2 : Pass(),
    # behringer   : Pass(),
    
})
