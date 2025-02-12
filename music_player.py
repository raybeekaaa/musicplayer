import pygame
class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_track = None
        self.playing = False
        self.volume = 0.5
        self.repeat = False
        self.tracks = []
        self.current_track_index = 0 

    def load_track(self, track_path):
        try:
            pygame.mixer.music.load(track_path)
            self.current_track = track_path
            return True
        except pygame.error:
            print(f"Error loading track: {track_path}")
            return False

    def play(self): 
        if self.current_track:
            pygame.mixer.music.play()
            self.playing = True
            if self.repeat:
                pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)

    def pause(self):
        if self.playing:
            pygame.mixer.music.pause()
            self.playing = False

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False
        self.current_track = None

    def get_current_track(self):
        return self.current_track

    def set_volume(self, volume):
        self.volume = max(0, min(1, volume)) 
        pygame.mixer.music.set_volume(self.volume)

    def get_volume(self):
        return self.volume

    def toggle_repeat(self):
        self.repeat = not self.repeat
        if self.repeat:
            pygame.mixer.music.set_endevent(self.on_repeat_end)
        else:
            pygame.mixer.music.set_endevent(None) 

    def on_repeat_end(self): 
        if self.repeat:
            self.play()

    def is_playing(self):
        return self.playing

    def set_track_list(self, tracks):
        self.tracks = tracks
        self.current_track_index = 0
        if self.tracks:
            self.load_track(self.tracks[0])

    def get_next_track(self):
        if self.tracks:
            self.current_track_index = (self.current_track_index + 1) % len(self.tracks)
            return self.tracks[self.current_track_index]
        return None

    def get_previous_track(self):
        if self.tracks:
            self.current_track_index = (self.current_track_index - 1) % len(self.tracks)
            return self.tracks[self.current_track_index]
        return None