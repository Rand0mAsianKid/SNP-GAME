"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
import random

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Starting Template"

MONSTER_SPAWN_INTERVAL = 3.0   
MONSTER_SPEED = 3            
MONSTER_VERTICAL_SPEED = 2     


class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()

        #self.background_color = arcade.color.AMAZON
        self.background_texture = arcade.load_texture("assets/purps.png")
        # Load the image file as a reusable texture

        # 1. Create a container to hold your sprites
        self.player_list = arcade.SpriteList()
<<<<<<< Updated upstream

    
        self.player_sprite = arcade.Sprite("assets/butler.png", scale=0.15)
=======
        
        # 2. Load the image into a Sprite object
        # Pass the image path and an optional scale factor
        self.player_sprite = arcade.Sprite("assets/char1.png", scale=0.15)
>>>>>>> Stashed changes
        self.player_list.append(self.player_sprite)

        self.player_sprite.center_x = WINDOW_WIDTH / 2
        self.player_sprite.center_y = WINDOW_HEIGHT / 2

        self.monster_list = arcade.SpriteList()

        self.time_since_last_spawn = 0.0

    def reset(self):
        """Reset the game to the initial state."""
        pass

    def spawn_monster(self):
        """Create one monster on the left or right edge, moving toward the other side."""
        monster = arcade.Sprite("assets/monster.png", scale=0.15)

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
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
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
                monster.change_y = abs(monster.change_y)   # force it to move up
            elif monster.center_y >= WINDOW_HEIGHT:
                monster.center_y = WINDOW_HEIGHT
                monster.change_y = -abs(monster.change_y)  # force it to move down

        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.monster_list)

        if hit_list:
            print("You bumped into the monster!")

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == arcade.key.LEFT:
            print("The left arrow key is pressed")
            self.player_sprite.change_x = -5
            self.player_sprite.scale_x = -abs(self.player_sprite.scale_x)

        if key == arcade.key.RIGHT:
            print("The right arrow key is pressed")
            self.player_sprite.change_x = 5
            self.player_sprite.scale_x = abs(self.player_sprite.scale_x)

        if key == arcade.key.UP:
            print("The up arrow key is pressed")
            self.player_sprite.change_y = 5
            self.player_sprite.scale_y = abs(self.player_sprite.scale_y)

        if key == arcade.key.DOWN:
            print("The down arrow key is pressed")
            self.player_sprite.change_y = -5
            #self.player_sprite.scale_y = -abs(self.player_sprite.scale_y)

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and setup the GameView
    game = GameView()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()