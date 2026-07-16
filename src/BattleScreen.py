"""
BattleScreen.py
"""
import arcade

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
        self.monster_sprite = arcade.Sprite("assets/monster.png", scale=0.4)
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

        arcade.draw_rect_filled(
            arcade.XYWH(self.button_center_x, self.button_center_y,
                        self.button_width, self.button_height),
            arcade.color.WHITE
        )
        arcade.draw_rect_outline(
            arcade.XYWH(self.button_center_x, self.button_center_y,
                        self.button_width, self.button_height),
            arcade.color.BLACK, border_width=4
        )
        arcade.draw_text(
            "ATTACK",
            self.button_center_x, self.button_center_y,
            arcade.color.BLACK, font_size=32,
            anchor_x="center", anchor_y="center", bold=True
        )

        arcade.draw_text(
            self.message,
            WINDOW_WIDTH / 2, self.button_center_y + 90,
            arcade.color.WHITE, font_size=20,
            anchor_x="center", anchor_y="center", bold=True
        )

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

        self.message = f"Click the attack button to battle!"


if __name__ == "__main__":
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "Battle Screen Test")
    battle_view = Battle()
    window.show_view(battle_view)
    arcade.run()