    
# --------------------------------------------------------------------
# Helper functions available for patches and controllers
# --------------------------------------------------------------------

with open("config.json") as FILE:
    config = json.load(FILE)
    
    
# Glissando -------------------------------------------------------------------------------------------

def glissando_process(ev, from_note, to_note, vel, duration, direction, port, on):
    output_event(NoteOnEvent(port, ev.channel, from_note, vel)) if on else output_event(NoteOffEvent(port, ev.channel, from_note))
    if not on:
        from_note += 1
    if from_note < to_note:
        Timer(duration, lambda: glissando_process(ev, from_note, to_note, vel, duration, direction, port, not on)).start()

def glissando(ev, from_note, to_note, vel, duration, direction, port):
    glissando_process(ev, from_note, to_note, vel, duration, direction, port, True)

# -------------------------------------------------------------------------------------------

# Create a pitchbend from a filter logic
# Params : direction when 1 bend goes UP, when -1 bend goes down
#          dont set direction with other values than 1 or -1 dude !
# NOTES  : On my context, ev.value.min = 0 and ev.value.max = 127
def OnPitchbend(ev, direction):
    if 0 < ev.value <= 126:
        return PitchbendEvent(ev.port, ev.channel, ((ev.value + 1) * 64) * direction)
    elif ev.value == 0:
        return PitchbendEvent(ev.port, ev.channel, 0)
    elif ev.value == 127:
        ev.value = 8191 if direction == 1 else 8192
    return PitchbendEvent(ev.port, ev.channel, ev.value * direction)

# ---------------------------------------------------------------------------------------------------------
''' Set or overwrite an environment variable '''
def setenv(ev, key, value):
    os.environ[key] = value

# ---------------------------------------------------------------------------------------------------------
