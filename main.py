from music_player import MusicPlayer
from music_libraries import MusicLibrary, PlaylistManager
from ui import MusicPlayerUI
import tkinter as tk

def main():
    try:
        root = tk.Tk()

        player = MusicPlayer()
        library = MusicLibrary("D:/Python/spotify_clone/music") 
        playlist_manager = PlaylistManager()
        ui = MusicPlayerUI(root, player, library, playlist_manager)  
        player.set_track_list(library.get_tracks())
        root.mainloop()

    except FileNotFoundError as e:
        print(f"Error: Music directory not found: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()