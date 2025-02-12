import os

class PlaylistManager:
    def __init__(self):
        self.playlists = {"Default": []}
        
    def add_playlist(self, name):
        if name not in self.playlists:
            self.playlists[name] = []

    def add_song_to_playlist(self, playlist, song):
        if playlist in self.playlists:
            self.playlists[playlist].append(song)

    def get_playlist(self, playlist):
        return self.playlists.get(playlist, [])

    def get_all_playlists(self):
        return list(self.playlists.keys())
    
    def save_playlists(self, filename="playlists.dat"):
        try:
            with open(filename, "wb") as f:
                pickle.dump(self.playlists, f)
            print("Playlists saved.") 
        except Exception as e:
            print(f"Error saving playlists: {e}")

    def load_playlists(self, filename="playlists.dat"):
        try:
            with open(filename, "rb") as f:
                self.playlists = pickle.load(f)
            print("Playlists loaded.") 
        except FileNotFoundError:
            print("No saved playlists found. Starting with default.")
        except Exception as e:
            print(f"Error loading playlists: {e}")

class MusicLibrary:
    def __init__(self, music_directory):
        self.music_directory = music_directory
        self.tracks = self.scan_directory()

    def scan_directory(self):
        tracks = []
        for root, dirs, files in os.walk(self.music_directory):
            for file in files:
                if file.lower().endswith(('.mp3', '.wav', '.flac', '.ogg', '.m4a')):
                    tracks.append(os.path.join(root, file))
        return tracks

    def get_tracks(self):
        return self.tracks