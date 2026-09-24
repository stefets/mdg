from rich.columns import Columns
from rich.console import Group
from rich.live import Live
from rich.progress_bar import ProgressBar
from rich.table import Table
from rich.text import Text


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
        adapter_table = Table(title="MIDIDINGS", title_justify="left")

        adapter_table.add_column("MPV")
        adapter_table.add_column("Volume", width=19)
        adapter_table.add_column("Jump")
        adapter_table.add_column("Paused", justify="center")
        adapter_table.add_column("Muted", justify="center")
        adapter_table.add_column("Loop", justify="center")
        adapter_table.add_column("Auto-next", justify="center")
        adapter_table.add_column("Song")

        for adapter in self.adapters:
            volume = Columns(
                [
                    ProgressBar(total=100, completed=adapter.volume, width=12),
                    Text(f" {adapter.volume:.0f}%")
                ],
                expand=False,
                padding=(0, 0),
            )
            adapter_table.add_row(
                adapter.address,
                volume,
                f"{adapter.jump_offset}s",
                self.indicator(adapter.paused, "yellow"),
                self.indicator(adapter.muted, "red"),
                self.indicator(adapter.loop, "green"),
                self.indicator(adapter.autonext, "green"),
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
                    song.name,
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

    def indicator(self, value, color):
        return f"[{color}]●[/{color}]" if value else "[dim]○[/dim]"