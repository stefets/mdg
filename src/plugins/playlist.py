from pathlib import Path
from mididings.engine import scenes, current_scene

class PlaylistManager:
    def __init__(self, terminal):
        self.playlist = Playlist()
        self.terminal = terminal
        self.terminal.register_playlist(self.playlist)
        self.has_subscene = None

    def __call__(self, ev):
        scene = self.get_scene_name()
        self.playlist.create(f"/media/soundlib/{scene}")
        self.terminal.refresh()

    def get_scene_name(self):
        return scenes()[current_scene()][0]


class Playlist:
    EXTENSIONS = {
        ".mp3",
        ".wav",
        ".flac",
        ".ogg",
        ".opus",
        ".m4a",
        ".aac",
        ".mp4",
        ".mkv",
        ".webm",
    }
    
    def __init__(self):
        self.songs = []

    def create(self, path):
        self.songs = [
            p.resolve()
            for p in sorted(Path(path).glob("**/*"))
            if p.is_file() and p.suffix.lower() in self.EXTENSIONS
        ]
  
    def len(self):
        return len(self.songs)

