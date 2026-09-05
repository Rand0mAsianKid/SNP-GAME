"""
ui_panels.py

Two pop-up panels built on arcade.gui, meant to be shown/hidden on top of
whichever View is currently active (PlayScreen uses both):

  ShopPanel     - spend coins on permanent power-ups (game_state.POWER_UP_DEFS)
  SettingsPanel - a draggable slider for text size, plus music volume/mute

Both inherit from ModalPanel, which dims the screen behind them and -- via
UIMouseFilterMixin -- swallows every click that lands anywhere on it. That's
what stops a click from "passing through" the popup into the game world
underneath (e.g. accidentally moving the player or re-triggering the button
that opened the popup).
"""
import arcade
from arcade.gui import (
    UIAnchorLayout,
    UIBoxLayout,
    UIFlatButton,
    UILabel,
    UIMouseFilterMixin,
    UIOnChangeEvent,
    UISlider,
)

from game_state import state, POWER_UP_DEFS
from audio_manager import music_manager

PANEL_BG = (52, 40, 30, 245)
PANEL_BORDER = (198, 152, 80)
TEXT_LIGHT = (240, 230, 210)
TEXT_MUTED = (200, 185, 165)
ACCENT_GOLD = (230, 190, 90)


def _clear_layout(layout):
    """Remove every child from a UIBoxLayout. There's no bulk clear() in
    arcade's gui, so we just remove them one at a time."""
    for child in list(layout.children):
        layout.remove(child)


class ModalPanel(UIMouseFilterMixin, UIAnchorLayout):
    """Full-window overlay that dims the background and blocks clicks from
    reaching whatever is behind it. Subclasses add their own content box,
    anchored center, inside __init__."""

    def __init__(self, window_width, window_height):
        super().__init__(width=window_width, height=window_height)
        self.with_background(color=(15, 12, 10, 175))


class ShopPanel(ModalPanel):
    """The power-up store. Call .refresh() any time game_state changes
    (currency spent, a level bought, text scale changed) so the panel's
    text stays in sync -- it's cheap enough to just rebuild from scratch."""

    def __init__(self, window_width, window_height, on_close):
        super().__init__(window_width, window_height)
        self.on_close = on_close

        self.box = UIBoxLayout(vertical=True, space_between=14)
        self.box.with_padding(all=26)
        self.box.with_background(color=PANEL_BG)
        self.box.with_border(color=PANEL_BORDER, width=3)

        self.add(self.box, anchor_x="center", anchor_y="center")

        self._status_label = None
        self.refresh()

    def refresh(self):
        _clear_layout(self.box)

        title = UILabel(text="STORE", font_size=state.scaled(26),
                         text_color=ACCENT_GOLD, bold=True)
        self.box.add(title)

        currency_label = UILabel(
            text=f"Your Coins: {state.currency}",
            font_size=state.scaled(16), text_color=TEXT_LIGHT,
        )
        self.box.add(currency_label)

        for power_id, info in POWER_UP_DEFS.items():
            self.box.add(self._build_row(power_id, info))

        self._status_label = UILabel(text=" ", font_size=state.scaled(13),
                                      text_color=ACCENT_GOLD)
        self.box.add(self._status_label)

        close_button = UIFlatButton(text="Close", width=140, height=42)
        close_button.on_click = self._on_close_click
        self.box.add(close_button)

        self.box.fit_content()

    def _build_row(self, power_id, info):
        level = state.power_up_levels[power_id]
        cost = state.power_up_cost(power_id)

        row = UIBoxLayout(vertical=False, space_between=16)

        text_col = UIBoxLayout(vertical=True, space_between=2)
        text_col.add(UILabel(
            text=f"{info['name']}  (Lv {level}/{info['max_level']})",
            font_size=state.scaled(15), text_color=TEXT_LIGHT, bold=True,
        ))
        text_col.add(UILabel(
            text=info["description"], font_size=state.scaled(12),
            text_color=TEXT_MUTED,
        ))
        text_col.fit_content()
        row.add(text_col)

        if cost is None:
            buy_button = UIFlatButton(text="MAXED", width=110, height=40)
            buy_button.disabled = True
        else:
            buy_button = UIFlatButton(text=f"Buy ({cost})", width=110, height=40)
            buy_button.on_click = self._make_buy_handler(power_id)
        row.add(buy_button)

        row.fit_content()
        return row

    def _make_buy_handler(self, power_id):
        def handler(event):
            success, message = state.buy_power_up(power_id)
            self.refresh()
            self._status_label.text = message
            self._status_label.fit_content()
        return handler

    def _on_close_click(self, event):
        self.on_close()


class SettingsPanel(ModalPanel):
    """Text-size slider + music controls. Both take effect immediately:
    the slider updates game_state.text_scale live (screens built after
    this point read the new size), and the music controls talk straight
    to the shared music_manager."""

    def __init__(self, window_width, window_height, on_close):
        super().__init__(window_width, window_height)
        self.on_close = on_close

        self.box = UIBoxLayout(vertical=True, space_between=18)
        self.box.with_padding(all=26)
        self.box.with_background(color=PANEL_BG)
        self.box.with_border(color=PANEL_BORDER, width=3)

        self.add(self.box, anchor_x="center", anchor_y="center")

        self._text_value_label = None
        self._music_toggle_button = None
        self.refresh()

    def refresh(self):
        _clear_layout(self.box)

        title = UILabel(text="SETTINGS", font_size=state.scaled(24),
                         text_color=ACCENT_GOLD, bold=True)
        self.box.add(title)

        # ---- text size row ----
        text_row = UIBoxLayout(vertical=False, space_between=14)
        text_row.add(UILabel(text="Text Size", width=120,
                              font_size=state.scaled(15), text_color=TEXT_LIGHT))

        size_slider = UISlider(
            value=round(state.text_scale * 100),
            min_value=75, max_value=175, step=5,
            width=220, height=22,
        )
        size_slider.on_change = self._on_text_size_change
        text_row.add(size_slider)

        self._text_value_label = UILabel(
            text=f"{round(state.text_scale * 100)}%", width=55,
            font_size=state.scaled(15), text_color=TEXT_LIGHT,
        )
        text_row.add(self._text_value_label)
        text_row.fit_content()
        self.box.add(text_row)

        # ---- music row ----
        music_row = UIBoxLayout(vertical=False, space_between=14)
        music_row.add(UILabel(text="Music", width=120,
                               font_size=state.scaled(15), text_color=TEXT_LIGHT))

        self._music_toggle_button = UIFlatButton(
            text="On" if state.music_enabled else "Off", width=70, height=36,
        )
        self._music_toggle_button.on_click = self._on_music_toggle
        music_row.add(self._music_toggle_button)

        volume_slider = UISlider(
            value=round(state.music_volume * 100),
            min_value=0, max_value=100, step=5,
            width=150, height=22,
        )
        volume_slider.on_change = self._on_volume_change
        music_row.add(volume_slider)
        music_row.fit_content()
        self.box.add(music_row)

        close_button = UIFlatButton(text="Close", width=140, height=42)
        close_button.on_click = self._on_close_click
        self.box.add(close_button)

        self.box.fit_content()

    def _on_text_size_change(self, event: UIOnChangeEvent):
        state.set_text_scale(event.new_value / 100)
        self._text_value_label.text = f"{round(event.new_value)}%"
        self._text_value_label.fit_content()

    def _on_music_toggle(self, event):
        enabled = music_manager.toggle_enabled()
        self._music_toggle_button.text = "On" if enabled else "Off"

    def _on_volume_change(self, event: UIOnChangeEvent):
        music_manager.set_volume(event.new_value / 100)

    def _on_close_click(self, event):
        self.on_close()