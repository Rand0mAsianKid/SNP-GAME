"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Starting Template"


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
        
        # 2. Load the image into a Sprite object
        # Pass the image path and an optional scale factor
        self.player_sprite = arcade.Sprite("assets/butler.png", scale=0.15)
        self.player_list.append(self.player_sprite)
        
        # 3. Position your sprite (X and Y coordinates)
        #self.player_sprite.center_x = 0
        #self.player_sprite.center_y = 0

        self.player_sprite.center_x = WINDOW_WIDTH / 2
        self.player_sprite.center_y = WINDOW_HEIGHT / 2

        # If you have sprite lists, you should create them here,
        # and set them to None

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background_texture, arcade.XYWH(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH-10, WINDOW_HEIGHT-10))
        self.player_list.draw()


    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.player_list.update()

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
            self.player_sprite.scale_y = -abs(self.player_sprite.scale_y)

        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        pass

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