from pathlib import Path
from mididings.engine import scenes, current_scene, current_subscene

class PlaylistManager:
    def __init__(self, terminal):
        self.playlist = Playlist()
        self.terminal = terminal
        self.terminal.register_playlist(self.playlist)
        self.has_subscene = None

    def __call__(self, ev):
        scene = self.get_scene_name()
        self.has_subscene = scenes()[current_scene()][1]
        subscene = self.get_subscene_name()
        path = f"{scene}/{subscene}" if subscene else scene
        self.playlist.create(f"/media/soundlib/{path}")
        self.terminal.refresh()

    def get_scene_name(self):
        return scenes()[current_scene()][0]

    def get_subscene_name(self):
        return (
            scenes()[current_scene()][1][current_subscene() - 1]
            if self.has_subscene
            else None
        )

class Playlist:
    AUDIO_EXTENSIONS = {
        ".mp3",
        ".wav",
        ".flac",
        ".ogg",
        ".opus",
        ".m4a",
        ".aac",
    }
    
    def __init__(self):
        self.songs = []

    def create(self, path):
        self.songs = [
            p.resolve()
            for p in sorted(Path(path).glob("**/*"))
            if p.is_file() and p.suffix.lower() in self.AUDIO_EXTENSIONS
        ]
  
    def len(self):
        return len(self.songs)

