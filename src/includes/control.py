
#
# Patches for the run().control patch
#

# Transport filter Filter for MPG123 and Spotipy and VLC
jump_filter    = CtrlFilter(1)  >> CtrlValueFilter(0, 121)
volume_filter  = CtrlFilter(7)  >> CtrlValueFilter(0, 101)
trigger_filter = Filter(NOTEON) >> Transpose(-36)
transport_filter = [jump_filter, volume_filter, trigger_filter]

mpg123_control_1 = transport_filter >> MPG123_SD90_A
mpg123_control_2 = transport_filter >> MPG123_SD90_B
vlc_control_1 = trigger_filter >> VLC_BASE

# Spotify
spotify_control = [
  trigger_filter,
  volume_filter, 
  CtrlFilter(44),
] >> Call(SpotifyPlayer())

mpk_soundcraft_control=Filter(CTRL|NOTE) >> [
        Filter(CTRL) >> Pass(),
        Filter(NOTE) >> NoteOn(EVENT_NOTE, 127) >> Port(midimix_midi),
    ] >> soundcraft_control


# Midi input control patch
control_patch = PortSplit({
    midimix_midi : soundcraft_control,
    mpk_midi : ChannelSplit({
        4 : mpg123_control_2,
    }),
    mpk_port_a : ChannelSplit({
         1 : CakewalkController,
         8 : mpg123_control_1,
         4 : mpg123_control_2,
        12 : vlc_control_1,
        13 : p_hue,
    }),
    mpk_port_b : ChannelSplit({
         1 : Program(sd90_port_a, EVENT_CHANNEL, EVENT_VALUE),
         8 : mpg123_control_1,
         4 : mpg123_control_2,
    }),
    sd90_midi_1 : Pass(),
    sd90_midi_2 : Pass(),
    behringer   : Pass(),
})
