from rich.live import Live
from rich.table import Table


class TerminalUI:

    def __init__(self):
        self.adapters = []
        self.volume = 46
        self.jump = 14
        self.auto_next = False

    def register(self, adapter):
        self.adapters.append(adapter)

    def render(self):
        table = Table(title="MIDIDINGS")

        table.add_column("Property")
        table.add_column("Value")

        table.add_row("Volume", f"{self.volume}%")
        table.add_row("Jump", f"{self.jump}s")
        table.add_row("Auto-next", str(self.auto_next))

        return table

    def start(self):
        self.live = Live(
            self.render(),
            refresh_per_second=10,
        )
        self.live.start()

    def stop(self):
        self.live.stop()