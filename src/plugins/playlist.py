import os
from pathlib import Path
from mididings.engine import scenes, current_scene
from typing import ClassVar


class PlaylistManager:
    def __init__(self, terminal):
        self.playlist = Playlist()
        self.terminal = terminal
        self.terminal.register_playlist(self.playlist)
        self.has_subscene = None

    def __call__(self, ev):
        scene = self.get_scene_name()
        self.playlist.create(f"{os.environ['MEDIA_LIB']}/{scene}")
        self.terminal.refresh()

    def get_scene_name(self):
        return scenes()[current_scene()][0]


class Playlist:
    audio_extensions: ClassVar[set[str]] = {
        ".mp3", ".wav", ".flac", ".ogg", ".opus", ".m4a", ".aac",
    }
    video_extensions: ClassVar[set[str]] = {".mp4", ".mkv", ".webm"}
    image_extensions: ClassVar[set[str]] = {".jpg", ".png"}

    audio_keys: ClassVar[range] = range(13, 75)
    video_keys: ClassVar[range] = range(75, 100)
    image_keys: ClassVar[range] = range(100, 128)

    def __init__(self):
        self.songs = []
        self.videos = []
        self.images = []

    def create(self, path):
        files = [
            p.resolve()
            for p in sorted(Path(path).glob("**/*"))
            if p.is_file()
        ]

        self.songs = self._create_items(
            files, self.audio_extensions, self.audio_keys
        )
        self.videos = self._create_items(
            files, self.video_extensions, self.video_keys
        )
        self.images = self._create_items(
            files, self.image_extensions, self.image_keys
        )

    @staticmethod
    def _create_items(files, extensions, keys):
        paths = [p for p in files if p.suffix.lower() in extensions]

        if len(paths) > len(keys):
            raise ValueError(
                f"Too many media files: {len(paths)} found, "
                f"maximum is {len(keys)}."
            )

        return [
            PlaylistItem(path, key)
            for path, key in zip(paths, keys)
        ]

class PlaylistItem:
    def __init__(self, path, key):
        self.key = key
        self.path = path
        self.name = Path(path).stem
