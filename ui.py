import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from music_libraries import MusicLibrary, PlaylistManager  
from music_player import MusicPlayer
import pygame



class MusicPlayerUI:
    def __init__(self, root, player, library, playlist_manager):
        self.root = root
        self.player = player
        self.library = library
        self.playlist_manager = playlist_manager
        self.playlist_manager.load_playlists()

        self.playlists = self.playlist_manager.playlists
       
        if "Default" not in self.playlists:
            self.playlists["Default"] = self.library.get_tracks()
            self.playlist_manager.add_playlist("Default")  # Add to PlaylistManager
        else:  # If default exists, update it if you wish.
            self.playlists["Default"] = self.library.get_tracks()
            self.playlist_manager.playlists["Default"] = self.library.get_tracks()

        self.current_playlist = "Default"
        self.player.set_track_list(self.playlists["Default"])
        self.player.current_track_index = 0

        self.track_widgets = {}

        # UI Initialization (Moved all of this INSIDE __init__)
        self.sidebar_frame = ttk.Frame(root, style="TFrame", width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.main_frame = ttk.Frame(root, style="TFrame")
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(self.sidebar_frame, text="Your Library", anchor="w").pack(fill=tk.X, pady=10, padx=10)

        self.library_listbox = tk.Listbox(self.sidebar_frame, bg="#333", fg="#fff", selectbackground="#444")
        self.library_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.library_listbox.bind("<<ListboxSelect>>", self.select_playlist)

        for playlist_name in self.playlists:
            self.library_listbox.insert(tk.END, playlist_name)
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)  # Set up end event
        self.root.bind(pygame.USEREVENT + 1, self.on_track_end)
       
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TButton", background="#1DB954", foreground="#fff", font=("Arial", 10))
        style.configure("TLabel", background="#121212", foreground="#fff", font=("Arial", 12))
        style.configure("TFrame", background="#121212")
       
        self.selected_tracks = set()
       
        self.prev_image = ImageTk.PhotoImage(Image.open("D:/Python/spotify_clone/assets/prev.png"))
        self.play_image = ImageTk.PhotoImage(Image.open("D:/Python/spotify_clone/assets/play.png"))
        self.pause_image = ImageTk.PhotoImage(Image.open("D:/Python/spotify_clone/assets/pause.png"))
        self.next_image = ImageTk.PhotoImage(Image.open("D:/Python/spotify_clone/assets/next.png"))

        self.playlists = {"Default": library.get_tracks()}
        self.current_playlist = "Default"

        self.sidebar_frame = ttk.Frame(root, style="TFrame", width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.main_frame = ttk.Frame(root, style="TFrame")
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.add_playlist_button = ttk.Button(self.sidebar_frame, text="New Playlist", command=self.create_custom_playlist)
        self.add_playlist_button.pack(fill=tk.X, pady=5, padx=10)

        self.controls_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.controls_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)

        self.playlist_label = ttk.Label(self.main_frame, text="Playlist", anchor="center")
        self.playlist_label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        self.playlist_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.playlist_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.playlist_canvas = tk.Canvas(self.playlist_frame, bg="#121212")
        self.scrollbar = ttk.Scrollbar(self.playlist_frame, orient=tk.VERTICAL, command=self.playlist_canvas.yview)
        self.playlist_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.playlist_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.inner_frame = ttk.Frame(self.playlist_canvas, style="TFrame")
        self.inner_frame.bind("<Configure>", lambda e: self.playlist_canvas.configure(scrollregion=self.playlist_canvas.bbox("all")))
        self.playlist_canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
       
        self.track_label = ttk.Label(self.controls_frame, text="No track playing")
        self.track_label.pack(side=tk.LEFT, padx=10)

        self.prev_button = ttk.Button(self.controls_frame, image=self.prev_image, command=self.play_prev_track)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.play_button = ttk.Button(self.controls_frame, image=self.play_image, command=self.play_track)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = ttk.Button(self.controls_frame, image=self.pause_image, command=self.pause_track)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(self.controls_frame, image=self.next_image, command=self.play_next_track)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.volume_slider = ttk.Scale(self.controls_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.adjust_volume)
        self.volume_slider.set(50)
        self.volume_slider.pack(side=tk.RIGHT, padx=10)
       
        self.populate_track_list()

        for playlist_name in self.playlists:
            self.library_listbox.insert(tk.END, playlist_name)

    def populate_track_list(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.track_widgets = {}

        for track in self.playlists.get(self.current_playlist, []):
            frame = ttk.Frame(self.inner_frame, style="TFrame")
            frame.pack(fill=tk.X, padx=5, pady=2)

            short_track = track.split("/")[-1] if len(track) <= 30 else track.split("/")[-1][:27] + "..."
            label = ttk.Label(frame, text=short_track, anchor="w")
            label.pack(side=tk.LEFT, fill=tk.X, expand=True)

            select_button = ttk.Checkbutton(frame, command=lambda t=track: self.toggle_selection(t))
            select_button.pack(side=tk.RIGHT)

            self.track_widgets[track] = frame\
                
    def toggle_selection(self, track):
        if track in self.selected_tracks:
            self.selected_tracks.remove(track)
        else:
            self.selected_tracks.add(track)

    def create_custom_playlist(self):
        if self.selected_tracks:
            new_playlist_name = f"Custom Playlist {len(self.playlists) + 1}"

            selected_tracks_copy = list(self.selected_tracks).copy() 

            self.playlist_manager.add_playlist(new_playlist_name)
            for track in selected_tracks_copy: 
                self.playlist_manager.add_song_to_playlist(new_playlist_name, track)

            self.library_listbox.insert(tk.END, new_playlist_name)
            self.selected_tracks.clear()
            self.playlists = self.playlist_manager.playlists
            self.populate_track_list()

            self.player.set_track_list(self.playlists[new_playlist_name])
            self.player.current_track_index = 0

    def select_playlist(self, event):
        selected_index = self.library_listbox.curselection()
        if selected_index:
            self.current_playlist = self.library_listbox.get(selected_index)
            self.player.set_track_list(self.playlists[self.current_playlist])
            self.player.current_track_index = 0
            self.populate_track_list()
   
    def play_track(self, track_index=None): 
        if track_index is None:
            selected_index = self.get_selected_track_index()
        else:
            selected_index = track_index 

        if selected_index is not None:
            self.player.current_track_index = selected_index
            track_path = self.playlists[self.current_playlist][selected_index]
            if self.player.load_track(track_path):
                self.player.play()
                self.track_label.config(text=track_path.split("/")[-1])

    def play_next_track(self):
        if self.player.tracks:  
            next_index = (self.player.current_track_index + 1) % len(self.player.tracks)
            self.play_track(next_index)  

    def play_prev_track(self):
        if self.player.tracks:  
            prev_index = (self.player.current_track_index - 1) % len(self.player.tracks)
            self.play_track(prev_index) 

    def on_track_end(self, event):
        if not self.player.is_playing() and not self.player.repeat:
            self.play_next_track() 
         
    def get_selected_track_index(self):
        for i, track in enumerate(self.playlists.get(self.current_playlist, [])):
            frame = self.track_widgets.get(track)  
            if frame:
                checkbutton = next((c for c in frame.winfo_children() if isinstance(c, ttk.Checkbutton)), None)
                if checkbutton and checkbutton.instate(['selected']):
                    return i
        return None

    def pause_track(self):
        self.player.pause()

    def adjust_volume(self, volume):
        self.player.set_volume(float(volume) / 100)

    def on_closing(self):
        self.playlist_manager.save_playlists()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
