from rich.live import Live
from rich.table import Table
from rich.console import Group


class TerminalUI:

    def __init__(self):
        self.adapters = []
        self.live = Live(
            self.render(),
            refresh_per_second=10,
        )        

    def register_adapter(self, adapter):
        self.adapters.append(adapter)
        
    def register_playlist(self, playlist):
        self.playlist = playlist

    def render(self):
        adapter_table = Table(title="MIDIDINGS")

        adapter_table.add_column("MPV")
        adapter_table.add_column("Volume")
        adapter_table.add_column("Jump")
        adapter_table.add_column("Auto-next")
        adapter_table.add_column("Song")

        for adapter in self.adapters:
            adapter_table.add_row(
                adapter.address,
                f"{adapter.volume}%",
                f"{adapter.jump_offset}s",
                str(adapter.autonext),
                adapter.get_current_song() or "",
            )

        # -------------------------
        # Playlist
        # -------------------------
        playlist_table = Table(title="PLAYLIST")

        playlist_table.add_column("#")
        playlist_table.add_column("Song")

        if self.adapters:
            songs = self.playlist.songs

            for index, song in enumerate(songs, start=1):
                playlist_table.add_row(
                    str(index),
                    str(song),
                )

        return Group(
            adapter_table,
            playlist_table,
        )

    def start(self):
        self.live = Live(
            self.render(),
            refresh_per_second=10,
        )
        self.live.start()

    def stop(self):
        self.live.stop()
        
    def refresh(self):
        self.live.update(
            self.render()
        )