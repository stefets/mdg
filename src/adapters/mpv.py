import mididings.constants as _constants
from mididings.engine import (
    current_scene,
    current_subscene,
    scenes,
    switch_scene,
    switch_subscene,
)
from range_key_dict import RangeKeyDict
from plugins.transport import Direction

from plugins.mpv import MpvClient


class MpvAdapter:
    def __init__(self, address: str, playlist, terminal):
        if address is None:
            raise ValueError("IPC socket path must be provided")

        self.address = address
        self.playlist = playlist
        self.terminal = terminal
        self.terminal.register_adapter(self)
        self.jump_offset = 10
        self.autonext = False
        self.current_entry = 0
        self.volume = 0
        self.paused = False
        self.muted = False
        self.loop = False
        
        # Offset for the note mapping, 
        # as the first 12 notes are reserved for scene navigation
        self.note_offset = 12  


        # Accepted range | Range array over the note_mapping array
        # Upper bound is exclusive
        self.note_range_mapping = RangeKeyDict(
            {
                (0, 5): self.navigate_scene,
                (5, 12): self.navigate_player,
                (12, 13): self.stop,
                (13, 128): self.on_play,
            }
        )

        # NoteOn mapping
        self.note_mapping = {
            0: self.prev_scene,
            1: self.prev_subscene,
            2: self.home_scene,
            3: self.next_subscene,
            4: self.next_scene,
            # White keys
            5: self.backward,
            7: self.toggle_autonext,
            9: self.on_toggle_loop,
            11: self.forward,
            # Black keys
            6: self.prev_entry,
            8: self.on_toggle_pause,
            10: self.next_entry,
        }

        # Control change mapping
        self.ctrl_mapping = {
                1: self.set_seek,
                2: self.on_toggle_mute,
                7: self.set_volume,
            }
        
        # The MPV client instance
        self.mpv = MpvClient(address, self.mpv_event_callback)
        self.mpv.volume(75.0)
        

    # call from mididings
    def __call__(self, ev):
        self.ctrl_mapping[ev.data1](
            ev
        ) if ev.type == _constants.CTRL else self.note_range_mapping[ev.data1](ev)

    # Event from MpvClient
    def mpv_event_callback(self, message):
        event_name = message.get("event")
        if event_name == "end-file":
            if message.get("reason") == "eof":
                if self.autonext:
                    self.load_current_entry(self.current_entry + 1)
                else:
                    pass
        elif event_name == "property-change":
            if message.get("name") == "volume":
                self.volume = message.get("data")
            elif message.get("name") == "pause":
                self.paused = message.get("data")
            elif message.get("name") == "mute":
                self.muted = message.get("data")
            elif message.get("name") == "loop-file":
                self.loop = message.get("data") == "inf"
        elif event_name == "start-file":
            pass  # No action but need a refresh to update the terminal with the current song
        else:
            print(f"Unhandled event: {message}")

        self.terminal.refresh()

    # Logic
    def navigate_scene(self, ev):
        self.note_mapping[ev.data1](ev)

    def navigate_player(self, ev):
        if self.playlist.songs:
            self.note_mapping[ev.data1](ev)

    # Unassigned key
    def unassigned(self, ev):
        pass

    def on_toggle_loop(self, ev):
        self.mpv.toggle_loop()
    
    def enable_autonext(self, ev):
        self.set_autonext(True)

    def disable_autonext(self, ev):
        self.set_autonext(False)

    def toggle_autonext(self, ev):
        self.set_autonext(not self.autonext)

    def set_autonext(self, value):
        self.autonext = value
        self.terminal.refresh()

    # Scenes navigation
    def home_scene(self, ev):
        self.set_scene(1)

    def set_scene(self, index):
        switch_scene(index)

    def next_scene(self, ev):
        self.on_switch_scene(Direction.Forward)

    def prev_scene(self, ev):
        self.on_switch_scene(Direction.Backward)

    def on_switch_scene(self, direction):
        offset = 1 if direction == Direction.Forward else -1
        keys = list(scenes().keys())
        index = keys.index(current_scene()) + offset

        # Go to first or last scene
        if index < 0:
            # Switch to last scene if the index is before the first scene
            key = keys[-1]
        elif index > len(scenes()) - 1:
            # Switch to first scene if the index is after the last scene
            key = keys[0]
        else:
            # Normal switch
            key = keys[index]

        switch_scene(key)

        self.current_entry = 0

    def next_subscene(self, ev):
        self.on_switch_subscene(Direction.Forward)

    def prev_subscene(self, ev):
        self.on_switch_subscene(Direction.Backward)

    def on_switch_subscene(self, direction):
        offset = 1 if direction == Direction.Forward else -1
        switch_subscene(current_subscene() + offset)
        self.current_subscene = current_subscene()
        self.current_entry = 0

    def on_play(self, ev):
        index = ev.data1 - self.note_offset
        self.load_current_entry(index)

    def load_current_entry(self, key):
        if 1 <= key <= 74:
            playlist = self.playlist.songs
        elif 75 <= key <= 99:
            playlist = self.playlist.videos
        elif 100 <= key <= 127:
            playlist = self.playlist.images
        else:
            print(f"Invalid media key: {key}")
            return

        item = next((item for item in playlist if item.key == key), None)

        if item is None:
            print(f"No media found for key {key}")
            return
        self.current_entry = key

        self.mpv.unpause()
        self.mpv.load(str(item.path))

    def on_toggle_pause(self, ev):
        """Pause if playing, else resume if paused"""
        self.mpv.toggle_pause()

    def on_toggle_mute(self, ev):
        """Mute or UnMute if playing"""
        if ev.data2 == 0:
            self.mpv.unmute()
        elif ev.data2 == 127:
            self.mpv.mute()
        else:
            print(f"Invalid CC value [{ev.data2}] for mute/unmute.")

    def forward(self, ev):
        self.on_seek(Direction.Forward)

    def backward(self, ev):
        self.on_seek(Direction.Backward)

    def on_seek(self, direction):
         self.mpv.seek(self.jump_offset) if direction == Direction.Forward else self.mpv.seek(-self.jump_offset)

    def next_entry(self, ev):
        ev.data1 = self.current_entry + 1 + self.note_offset
        self.on_play(ev)

    def prev_entry(self, ev):
        ev.data1 = self.current_entry - 1 + self.note_offset
        self.on_play(ev)

    def set_volume(self, ev):
        if ev.data2 % 2 != 0:
            return
        self.mpv.volume(ev.data2)

    def set_seek(self, ev):
        jump = int(ev.data2 / 2)
        if jump % 2 == 0:
            self.jump_offset = jump
        self.terminal.refresh()

    def get_current_song(self):
        key = self.current_entry
        if 1 <= key <= 74:
            playlist = self.playlist.songs
        elif 75 <= key <= 99:
            playlist = self.playlist.videos
        elif 100 <= key <= 127:
            playlist = self.playlist.images
        else:
            #print(f"Invalid media key: {key} - get_current_song()")
            return

        item = next((item for item in playlist if item.key == key), None)

        if item is None:
            print(f"No media found for key {key}")
            return
        try:
            if self.current_entry > 0:
                return f"{self.current_entry}-{item.name}"
        except IndexError:
            return "IndexError"

    def on_replay(self, ev):
        if self.current_entry > 0:
            # TODO: Replay the current entry
            pass
            # self.mpv.load_list(self.current_entry, self.playlist.filename)

    def stop(self, ev):
        self.mpv.stop()