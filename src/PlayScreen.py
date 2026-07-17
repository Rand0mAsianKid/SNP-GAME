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
import random

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Starting Template"

MONSTER_SPAWN_INTERVAL = 3.0
MONSTER_SPEED = 3
MONSTER_VERTICAL_SPEED = 2


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

        self.time_since_last_spawn = 0.0

        # Pre-build the Battle view up front. If we waited and built it
        # at the moment of collision, any texture/asset loading inside
        # Battle.__init__ would happen mid-frame — that's the "delay".
        self.battle_view = Battle()

    def reset(self):
        """Reset the game to the initial state."""
        pass

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

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background_texture,
            arcade.XYWH(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH - 10, WINDOW_HEIGHT - 10)
        )
        self.player_list.draw()
        self.monster_list.draw()

    def on_update(self, delta_time):
        self.player_list.update()
        self.monster_list.update()

        self.time_since_last_spawn += delta_time
        if self.time_since_last_spawn >= MONSTER_SPAWN_INTERVAL:
            self.spawn_monster()
            self.time_since_last_spawn = 0.0

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
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -5
            self.player_sprite.scale_x = -abs(self.player_sprite.scale_x)

        if key == arcade.key.RIGHT:
            self.player_sprite.change_x = 5
            self.player_sprite.scale_x = abs(self.player_sprite.scale_x)

        if key == arcade.key.UP:
            self.player_sprite.change_y = 5
            self.player_sprite.scale_y = abs(self.player_sprite.scale_y)

        if key == arcade.key.DOWN:
            self.player_sprite.change_y = -5

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