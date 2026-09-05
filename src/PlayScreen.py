"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import time

from BattleScreen import Battle
import arcade
import arcade.gui
import random

from PIL import Image, ImageDraw

from game_state import state
from audio_manager import music_manager, MUSIC_PATH, COIN_SOUND_PATH
from ui_panels import ShopPanel, SettingsPanel

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Starting Template"

MONSTER_SPAWN_INTERVAL = 3.0
MONSTER_SPEED = 3
MONSTER_VERTICAL_SPEED = 2

PLAYER_BASE_SPEED = 5

COIN_VALUE = 15
COIN_SPAWN_INTERVAL = 4.0
COIN_LIFETIME = 9.0  # seconds an uncollected coin sits around before vanishing


def make_coin_texture(diameter=36):
    """Draws a simple shiny gold coin with PIL, the same way the quiz
    screen builds its button textures -- no external art asset needed."""
    img = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    gradient = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(gradient)

    top = (255, 226, 130)
    bottom = (196, 140, 35)
    for y in range(diameter):
        t = y / diameter
        r = int(top[0] * (1 - t) + bottom[0] * t)
        g = int(top[1] * (1 - t) + bottom[1] * t)
        b = int(top[2] * (1 - t) + bottom[2] * t)
        gdraw.line([(0, y), (diameter, y)], fill=(r, g, b, 255))

    margin = 2
    mask = Image.new("L", (diameter, diameter), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse([margin, margin, diameter - margin - 1, diameter - margin - 1], fill=255)
    img.paste(gradient, (0, 0), mask)

    draw = ImageDraw.Draw(img)
    draw.ellipse(
        [margin, margin, diameter - margin - 1, diameter - margin - 1],
        outline=(120, 85, 20, 255), width=2,
    )
    inset = diameter // 5
    draw.ellipse(
        [inset, inset, diameter - inset - 1, diameter - inset - 1],
        outline=(255, 245, 200, 160), width=1,
    )
    draw.ellipse(
        [diameter * 0.22, diameter * 0.18, diameter * 0.52, diameter * 0.44],
        fill=(255, 255, 255, 90),
    )
    return img


COIN_TEXTURE = arcade.Texture(make_coin_texture())


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        self.background_texture = arcade.load_texture("assets/purps.png")

        self.player_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite("assets/char1.png", scale=0.5)
        self.player_list.append(self.player_sprite)

        self.player_sprite.center_x = WINDOW_WIDTH / 2
        self.player_sprite.center_y = WINDOW_HEIGHT / 2

        self.monster_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        self.time_since_last_spawn = 0.0
        self.time_since_last_coin = 0.0

        # Pre-build the Battle view up front. If we waited and built it
        # at the moment of collision, any texture/asset loading inside
        # Battle.__init__ would happen mid-frame — that's the "delay".
        self.battle_view = Battle()

        # ---------------------------------------------------------------
        # HUD + popups (Shop / Settings). One UIManager holds the always
        # -visible top bar buttons; the Shop/Settings panels are only
        # added to it while open, so they don't intercept clicks otherwise.
        # ---------------------------------------------------------------
        self.ui_manager = arcade.gui.UIManager()

        top_bar = arcade.gui.UIBoxLayout(vertical=False, space_between=12)

        self.shop_button = arcade.gui.UIFlatButton(text="Shop", width=110, height=42)
        self.shop_button.on_click = self.on_shop_button_click
        top_bar.add(self.shop_button)

        self.settings_button = arcade.gui.UIFlatButton(text="Settings", width=110, height=42)
        self.settings_button.on_click = self.on_settings_button_click
        top_bar.add(self.settings_button)

        top_bar.fit_content()

        top_anchor = arcade.gui.UIAnchorLayout()
        top_anchor.add(top_bar, anchor_x="right", anchor_y="top", align_x=-16, align_y=-16)
        self.ui_manager.add(top_anchor)

        self.shop_panel = ShopPanel(WINDOW_WIDTH, WINDOW_HEIGHT, on_close=self.close_shop)
        self.settings_panel = SettingsPanel(WINDOW_WIDTH, WINDOW_HEIGHT, on_close=self.close_settings)
        self.shop_open = False
        self.settings_open = False

    def reset(self):
        """Reset the game to the initial state."""
        pass

    # ------------------------------------------------------------ view --
    def on_show_view(self):
        """Enable the HUD's UI manager and (re)start the background music
        -- if a track is already playing, music_manager just lets it keep
        going instead of restarting it."""
        self.ui_manager.enable()
        music_manager.play(MUSIC_PATH)

    def on_hide_view(self):
        self.ui_manager.disable()

    # ------------------------------------------------------- shop/settings --
    def open_shop(self):
        self.close_settings()
        if not self.shop_open:
            self.shop_panel.refresh()
            self.ui_manager.add(self.shop_panel)
            self.shop_open = True

    def close_shop(self, event=None):
        if self.shop_open:
            self.ui_manager.remove(self.shop_panel)
            self.shop_open = False

    def open_settings(self):
        self.close_shop()
        if not self.settings_open:
            self.settings_panel.refresh()
            self.ui_manager.add(self.settings_panel)
            self.settings_open = True

    def close_settings(self, event=None):
        if self.settings_open:
            self.ui_manager.remove(self.settings_panel)
            self.settings_open = False

    def on_shop_button_click(self, event):
        self.close_shop() if self.shop_open else self.open_shop()

    def on_settings_button_click(self, event):
        self.close_settings() if self.settings_open else self.open_settings()

    # ---------------------------------------------------------- spawning --
    def spawn_monster(self):
        """Create one monster on the left or right edge, moving toward the other side."""
        imagegenerator = random.randint(0, 3)
        image = ["assets/one.png", "assets/two.png", "assets/three.png", "assets/four.png"]
        monster = arcade.Sprite(image[imagegenerator], scale=0.2)

        monster.center_y = random.randint(50, WINDOW_HEIGHT - 50)

        spawn_side = random.choice(["left", "right"])

        if spawn_side == "left":
            monster.center_x = -50
            monster.change_x = MONSTER_SPEED
        else:
            monster.center_x = WINDOW_WIDTH + 50
            monster.change_x = -MONSTER_SPEED

        monster.change_y = random.choice([-1, 1]) * MONSTER_VERTICAL_SPEED

        self.monster_list.append(monster)

    def spawn_coin(self):
        """Drop a coin at a random spot on the map. Walking into it adds
        currency (see on_update)."""
        margin = 60
        coin = arcade.Sprite(COIN_TEXTURE)
        coin.center_x = random.randint(margin, WINDOW_WIDTH - margin)
        coin.center_y = random.randint(margin, WINDOW_HEIGHT - margin)
        coin.lifetime = 0.0
        self.coin_list.append(coin)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background_texture,
            arcade.XYWH(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH - 10, WINDOW_HEIGHT - 10)
        )
        self.player_list.draw()
        self.monster_list.draw()
        self.coin_list.draw()

        arcade.draw_text(
            f"Coins: {state.currency}",
            24, WINDOW_HEIGHT - 44,
            arcade.color.GOLD, font_size=state.scaled(22), bold=True,
        )

        self.ui_manager.draw()

    def on_update(self, delta_time):
        self.player_list.update()
        self.monster_list.update()
        self.coin_list.update()

        self.time_since_last_spawn += delta_time
        if self.time_since_last_spawn >= MONSTER_SPAWN_INTERVAL:
            self.spawn_monster()
            self.time_since_last_spawn = 0.0

        self.time_since_last_coin += delta_time
        if self.time_since_last_coin >= COIN_SPAWN_INTERVAL:
            self.spawn_coin()
            self.time_since_last_coin = 0.0

        for monster in self.monster_list:
            if monster.center_x < -100 or monster.center_x > WINDOW_WIDTH + 100:
                monster.remove_from_sprite_lists()
                continue

            if monster.center_y <= 0:
                monster.center_y = 0
                monster.change_y = abs(monster.change_y)
            elif monster.center_y >= WINDOW_HEIGHT:
                monster.center_y = WINDOW_HEIGHT
                monster.change_y = -abs(monster.change_y)

        # Coins quietly expire if nobody grabs them in time, and get
        # collected (currency + a little "cha-ching") on contact.
        for coin in self.coin_list:
            coin.lifetime += delta_time
            if coin.lifetime >= COIN_LIFETIME:
                coin.remove_from_sprite_lists()

        coin_hits = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coin_hits:
            coin.remove_from_sprite_lists()
            state.add_currency(COIN_VALUE + state.coin_bonus)
            music_manager.play_sound_effect(COIN_SOUND_PATH)

        # Single collision check, done once per frame.
        hit_list = arcade.check_for_collision_with_list(
            self.player_sprite,
            self.monster_list
        )

        if hit_list:
            print("Player hit a monster!")
            # Switch to the already-built Battle view — no loading here,
            # so the transition is instant.
            self.window.show_view(self.battle_view)
            return  # stop this frame immediately, don't do more work after switching

    def on_key_press(self, key, key_modifiers):
        # Speed Boost (bought in the Shop) adds straight onto base speed.
        speed = PLAYER_BASE_SPEED + state.speed_bonus

        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -speed
            self.player_sprite.scale_x = -abs(self.player_sprite.scale_x)

        if key == arcade.key.RIGHT:
            self.player_sprite.change_x = speed
            self.player_sprite.scale_x = abs(self.player_sprite.scale_x)

        if key == arcade.key.UP:
            self.player_sprite.change_y = speed
            self.player_sprite.scale_y = abs(self.player_sprite.scale_y)

        if key == arcade.key.DOWN:
            self.player_sprite.change_y = -speed

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()