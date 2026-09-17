from rich.live import Live
from rich.table import Table


class TerminalUI:

    def __init__(self):
        self.adapters = []
        self.live = Live(
            self.render(),
            refresh_per_second=10,
        )        

    def register(self, adapter):
        self.adapters.append(adapter)

    def render(self):
        table = Table(title="MIDIDINGS")

        table.add_column("MPV")
        table.add_column("Volume")
        table.add_column("Jump")
        table.add_column("Auto-next")
        table.add_column("Song")

        for adapter in self.adapters:
            table.add_row(
                adapter.address,
                f"{adapter.volume}%",
                f"{adapter.jump_offset}s",
                str(adapter.autonext),
                adapter.get_current_song() or "",
            )

        return table

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