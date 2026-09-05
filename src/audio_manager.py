"""
Thin wrapper around arcade's sound system.

- MUSIC_PATH points at an example track (assets/music/theme.wav) generated
  purely from code -- no internet/download needed to try this out. Point
  MUSIC_PATH at your own .mp3/.ogg/.wav to replace it; arcade plays all
  three. (We shipped a .wav for the example specifically because looping
  mp3 playback depends on ffmpeg being available through pyglet -- .wav
  always works out of the box.)
- One `music_manager` singleton is shared by every screen, and each
  screen's on_show_view() just calls music_manager.play(). Because it
  remembers what's already playing, switching between PlayScreen /
  BattleScreen / LearnScreen does NOT restart the track from the
  beginning -- it just keeps looping underneath.
"""
import os
import arcade

from game_state import state

MUSIC_PATH = "assets/music/theme.wav"
COIN_SOUND_PATH = "assets/sounds/coin.wav"


class MusicManager:
    def __init__(self):
        self._sound = None
        self._player = None
        self._current_path = None
        self._sfx_cache = {}

    def play(self, path=MUSIC_PATH):
        """Start (or keep playing) a looping background track."""
        if not state.music_enabled:
            self._current_path = path  # remember what to resume later
            return

        if self._current_path == path and self._player is not None and self._is_playing():
            return  # already playing this exact track, don't restart it

        self.stop()

        if not os.path.exists(path):
            print(f"[audio] Music file not found: {path} (skipping music)")
            return

        try:
            # streaming=False so `loop=True` actually works -- arcade/pyglet
            # can't loop a streamed sound, only a fully-loaded one.
            self._sound = arcade.load_sound(path, streaming=False)
            self._player = self._sound.play(volume=state.music_volume, loop=True)
            self._current_path = path
        except Exception as exc:  # pragma: no cover - depends on system audio
            print(f"[audio] Could not play music ({path}): {exc}")

    def _is_playing(self):
        return bool(getattr(self._player, "playing", True))

    def stop(self):
        if self._player is not None:
            try:
                arcade.stop_sound(self._player)
            except Exception:
                pass
        self._player = None

    def set_volume(self, volume):
        state.music_volume = max(0.0, min(1.0, volume))
        if self._player is not None:
            self._player.volume = state.music_volume

    def toggle_enabled(self):
        """Mute/unmute. Returns the new enabled state."""
        state.music_enabled = not state.music_enabled
        if state.music_enabled:
            self.play(self._current_path or MUSIC_PATH)
        else:
            self.stop()
        return state.music_enabled

    def play_sound_effect(self, path=COIN_SOUND_PATH, volume=0.8):
        """One-shot effect (e.g. coin pickup) -- independent of the music."""
        if not os.path.exists(path):
            return
        try:
            if path not in self._sfx_cache:
                self._sfx_cache[path] = arcade.load_sound(path, streaming=False)
            self._sfx_cache[path].play(volume=volume)
        except Exception as exc:  # pragma: no cover - depends on system audio
            print(f"[audio] Could not play sound effect ({path}): {exc}")


# The single shared instance -- import THIS, not the class.
music_manager = MusicManager()