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

        self.paused = False
        self.muted = False
        self.volume = 100
        self.loop = False

        # The MPV client instance
        self.mpv = MpvClient(address, self.mpv_event_callback)
        self.mpv.volume(self.volume)

        # Accepted range | Range array over the note_mapping array
        # Upper bound is exclusive
        self.note_range_mapping = RangeKeyDict(
            {
                (0, 1): self.on_toggle_loop,
                (1, 36): self.on_play,
                (36, 41): self.navigate_scene,
                (41, 48): self.navigate_player,
                # (self.controller.size - 1, self.controller.size): self.on_replay,
            }
        )

        # NoteOn mapping
        self.note_mapping = {
            36: self.prev_scene,
            37: self.prev_subscene,
            38: self.home_scene,
            39: self.next_subscene,
            40: self.next_scene,
            # White keys
            41: self.backward,
            43: self.toggle_autonext,
            45: self.on_toggle_loop,
            47: self.forward,
            # Black keys
            42: self.prev_entry,
            44: self.on_toggle_pause,
            46: self.next_entry,
        }

        # Control change mapping
        self.ctrl_mapping = {
                1: self.set_seek,
                2: self.on_toggle_mute,
                7: self.set_volume,
            }

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
        self.on_switch_subscene(1)

    def prev_subscene(self, ev):
        self.on_switch_subscene(-1)

    def on_switch_subscene(self, offset):
        switch_subscene(current_subscene() + offset)
        self.current_subscene = current_subscene()
        self.current_entry = 0

    def on_play(self, ev):
        self.load_current_entry(ev.data1)

    def load_current_entry(self, index):
        if index > len(self.playlist.songs):
            print(
                f"Index {index} is out of range for playlist with {len(self.playlist.songs)} entries"
            )
            return

        self.current_entry = index

        self.mpv.unpause()  # Unpause before loading the file to ensure playback starts immediately
        self.mpv.load(str(self.playlist.songs[self.current_entry - 1]))

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
        if self.playlist.len() >= self.current_entry + 1:
            ev.data1 = self.current_entry + 1
            self.on_play(ev)

    def prev_entry(self, ev):
        if self.current_entry > 1:
            ev.data1 = self.current_entry - 1
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
        try:
            if self.current_entry > 0:
                return f"{self.current_entry}-{self.playlist.songs[self.current_entry - 1].name}"
        except IndexError:
            return "IndexError"

    def on_replay(self, ev):
        if self.current_entry > 0:
            # TODO: Replay the current entry
            pass
            # self.mpv.load_list(self.current_entry, self.playlist.filename)
