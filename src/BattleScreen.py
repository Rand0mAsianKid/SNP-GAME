"""
BattleScreen.py
"""
import arcade
import arcade.gui

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

PLAYER_MAX_HEALTH = 100
MONSTER_MAX_HEALTH = 50
PLAYER_ATTACK_DAMAGE = 10
MONSTER_ATTACK_DAMAGE = 8


class Battle(arcade.View):
    """
    Battle screen: char1.png vs monster.png
    """

    def __init__(self, forest_view=None):
        super().__init__()

        self.forest_view = forest_view

        self.background_texture = arcade.load_texture("assets/background.png")

        self.char_list = arcade.SpriteList()
        self.char_sprite = arcade.Sprite("assets/char1.png", scale=0.4)
        self.char_sprite.center_x = WINDOW_WIDTH * 0.25
        self.char_sprite.center_y = WINDOW_HEIGHT * 0.45
        self.char_list.append(self.char_sprite)

        self.monster_list = arcade.SpriteList()
        self.monster_sprite = arcade.Sprite("assets/one.png", scale=0.4)
        self.monster_sprite.center_x = WINDOW_WIDTH * 0.75
        self.monster_sprite.center_y = WINDOW_HEIGHT * 0.45
        self.monster_list.append(self.monster_sprite)

        self.player_health = PLAYER_MAX_HEALTH
        self.monster_health = MONSTER_MAX_HEALTH

        self.button_center_x = WINDOW_WIDTH / 2
        self.button_center_y = 120
        self.button_width = 260
        self.button_height = 80

        self.message = "Click ATTACK to fight!"
        self.battle_over = False

        # --- UI setup: a real button widget instead of a drawn rectangle ---
        self.ui_manager = arcade.gui.UIManager()

        self.attack_button = arcade.gui.UIFlatButton(
            text="ATTACK",
            width=self.button_width,
            height=self.button_height,
        )
        self.attack_button.on_click = self.on_attack_button_click

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(
            self.attack_button,
            anchor_x="center",
            anchor_y="bottom",
            align_x=0,
            align_y=self.button_center_y - self.button_height / 2,
        )
        self.ui_manager.add(anchor)

    def set_monster_texture(self, texture_path):
        """Swap the battle monster's sprite to match whichever mob was hit
        in the overworld, so the skin stays consistent between screens."""
        self.monster_sprite.texture = arcade.load_texture(texture_path)

    def on_show_view(self):
        """Called automatically when this view becomes the active one."""
        self.ui_manager.enable()

    def on_hide_view(self):
        """Called automatically when switching away from this view."""
        self.ui_manager.disable()

    def deal_damage_to_monster(self):
        """Apply one player attack's worth of damage to the monster.
        Called by the quiz screen after a correct answer, so the monster's
        health persists across multiple quiz rounds instead of resetting."""
        self.monster_health -= PLAYER_ATTACK_DAMAGE
        if self.monster_health <= 0:
            self.monster_health = 0
            self.battle_over = True
            self.message = "Monster defeated!"
        else:
            self.message = f"Hit! Monster health: {self.monster_health}"

    def on_attack_button_click(self, event):
        """Runs when the ATTACK button is clicked — go to the quiz screen,
        built fresh so it's a new random question each time. We pass
        ourselves in as battle_view so the quiz screen can report a
        correct answer back to THIS SAME battle instead of a new one,
        which is what actually makes the health bar go down."""
        from LearnScreen import GameView  # deferred import, avoids circular import
        self.window.show_view(GameView(battle_view=self))

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background_texture,
            arcade.XYWH(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        self.char_list.draw()
        self.monster_list.draw()

        self.draw_health_bar(
            x=40, y=WINDOW_HEIGHT - 60,
            width=250, height=25,
            current=self.player_health, max_health=PLAYER_MAX_HEALTH,
            label="YOU"
        )

        self.draw_health_bar(
            x=WINDOW_WIDTH - 290, y=WINDOW_HEIGHT - 60,
            width=250, height=25,
            current=self.monster_health, max_health=MONSTER_MAX_HEALTH,
            label="MONSTER"
        )

        arcade.draw_text(
            self.message,
            WINDOW_WIDTH / 2, self.button_center_y + 90,
            arcade.color.WHITE, font_size=20,
            anchor_x="center", anchor_y="center", bold=True
        )

        self.ui_manager.draw()

    def draw_health_bar(self, x, y, width, height, current, max_health, label):
        """Draws a label + background bar + colored fill for a health bar."""
        arcade.draw_text(label, x, y + height + 5, arcade.color.WHITE, font_size=14, bold=True)

        arcade.draw_rect_filled(
            arcade.XYWH(x + width / 2, y + height / 2, width, height),
            arcade.color.DARK_RED
        )

        fill_ratio = max(current, 0) / max_health
        fill_width = width * fill_ratio
        if fill_width > 0:
            arcade.draw_rect_filled(
                arcade.XYWH(x + fill_width / 2, y + height / 2, fill_width, height),
                arcade.color.GREEN
            )

        # Outline
        arcade.draw_rect_outline(
            arcade.XYWH(x + width / 2, y + height / 2, width, height),
            arcade.color.WHITE, border_width=2
        )


if __name__ == "__main__":
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "Battle Screen Test")
    battle_view = Battle()
    window.show_view(battle_view)
    arcade.run()