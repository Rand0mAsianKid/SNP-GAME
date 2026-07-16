"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import random

import arcade

import pyttsx3
import threading

from arcade.gui import (
    UIAnchorLayout,
    UIFlatButton,
    UIGridLayout,
    UIImage,
    UIOnChangeEvent,
    UITextureButton,
    UITextureToggle,
    UIView,
)
from matplotlib.pylab import matrix

import PlayScreen

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Starting Template"

TEX_RED_BUTTON_NORMAL = arcade.load_texture("assets/buttonalt.png")
TEX_RED_BUTTON_HOVER = arcade.load_texture("assets/button.png")
TEX_RED_BUTTON_PRESS = arcade.load_texture("assets/buttonalt.png")

engine1 = pyttsx3.init()

# ---------------------------------------------------------------------------
# Text-to-speech helper
#
# pyttsx3 is NOT thread-safe: only one runAndWait() loop can be active on a
# given engine at a time. Since we want speech triggered from button clicks
# (which can happen rapidly, or overlap with the question being read out at
# startup), we need to:
#   1. Serialize access with a Lock so two runAndWait() calls never run at once.
#   2. Call engine1.stop() BEFORE acquiring the lock, so if something is
#      already talking, it gets interrupted immediately instead of finishing
#      its sentence first.
# speak_async() takes any number of phrases and reads them in order within
# a single runAndWait() call (so "the answer" then "Correct!" read back to
# back, not as two separate overlapping speech sessions).
# ---------------------------------------------------------------------------
speech_lock = threading.Lock()


def speak_async(*phrases):
    engine1.stop()  # interrupt whatever is currently being read, if anything

    def _run():
        with speech_lock:
            for phrase in phrases:
                engine1.say(phrase)
            engine1.runAndWait()

    threading.Thread(target=_run, daemon=True).start()


try:
    arcade.load_font("assets/fonts/OpenDyslexic-Regular.ttf")
    arcade.load_font("assets/fonts/OpenDyslexic-Bold.ttf")
    FONT_NAME = ("OpenDyslexic", "arial", "calibri")
    FONT_NAME_BOLD = ("OpenDyslexic Bold", "OpenDyslexic", "arial", "calibri")
except FileNotFoundError:
    # Font files not found - fall back to system fonts so the game still runs
    FONT_NAME = ("arial", "calibri")
    FONT_NAME_BOLD = ("arial", "calibri")

# Centralized sizes so every piece of text stays consistent and large
QUESTION_FONT_SIZE = 36
BUTTON_FONT_SIZE = 15

questionList = [
    [
        "WHICH WORD MEANS HAPPY?",
        "SAD",
        "ANGRY",
        "GLAD",
        "TIRED",
        "SAD"
    ],
    [
        "WHICH SENTENCE IS CORRECT?",
        "THE DOG RUN FAST.",
        "THE DOG RUNS FAST.",
        "THE DOG RUNNING FAST.",
        "THE DOG RUNNED FAST.",
        "THE DOG RUN FAST."
    ],
    [
        "I DRINK _____ WHEN I AM THIRSTY.",
        "WATER",
        "CHAIR",
        "PENCIL",
        "SHOES",
        "WATER"
    ],
    [
        "WHICH WORD IS THE OPPOSITE OF BIG?",
        "TALL",
        "SMALL",
        "HEAVY",
        "WIDE",
        "SMALL"
    ],
    [
        "WHICH SENTENCE MAKES THE MOST SENSE?",
        "THE FISH CLIMBED A TREE.",
        "THE BIRD SWAM IN THE DESERT.",
        "THE CAT DRANK MILK.",
        "THE CAR ATE DINNER.",
        "THE CAT DRANK MILK."
    ]
]


class GameView(UIView):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()
        self.random_int = random.randint(1, 5)

        self.background_color = arcade.color.BISQUE

        # 1. Create a container to hold your sprites
        self.player_list = arcade.SpriteList()

        # Centered, large, bold question text.
        # - x is the window's horizontal midpoint
        # - anchor_x="center" makes that x value the text's center, not its
        #   left edge, so it stays centered regardless of text length
        # - width + align="center" also centers multi-line wrapped text
        self.question_text = arcade.Text(
            questionList[self.random_int - 1][0],
            x=WINDOW_WIDTH // 2,
            y=WINDOW_HEIGHT - 60,
            color=arcade.color.BLACK,
            font_size=QUESTION_FONT_SIZE,
            font_name=FONT_NAME_BOLD,
            bold=True,
            anchor_x="center",
            anchor_y="center",
            width=WINDOW_WIDTH - 100,
            align="center",
            multiline=True,
        )
        speak_async(questionList[self.random_int - 1][0])

        # 2. Build the UI layout
        grid = UIGridLayout(
            column_count=2,
            row_count=2,
            size_hint=(0, 0),
            vertical_spacing=70,
            horizontal_spacing=90,
        )

        # Style dict applied to every button state so the answer text is
        # large and uses the bold OpenDyslexic font. UITextureButton has no
        # separate "bold" flag - bolding is done by pointing font_name at an
        # actual bold font file/family, which is what FONT_NAME_BOLD does.
        button_style = {
            "normal": UITextureButton.UIStyle(
                font_size=BUTTON_FONT_SIZE,
                font_name=FONT_NAME_BOLD,
                font_color=arcade.color.BLACK,
            ),
            "hover": UITextureButton.UIStyle(
                font_size=BUTTON_FONT_SIZE,
                font_name=FONT_NAME_BOLD,
                font_color=arcade.color.DARK_BLUE,
            ),
            "press": UITextureButton.UIStyle(
                font_size=BUTTON_FONT_SIZE,
                font_name=FONT_NAME_BOLD,
                font_color=arcade.color.WHITE,
            ),
            "disabled": UITextureButton.UIStyle(
                font_size=BUTTON_FONT_SIZE,
                font_name=FONT_NAME_BOLD,
                font_color=arcade.color.GRAY,
            ),
        }

        texture_button_with_icon_left = UITextureButton(
            text=questionList[self.random_int - 1][1],
            multiline=True,
            width=500,
            texture=TEX_RED_BUTTON_NORMAL,
            texture_hovered=TEX_RED_BUTTON_HOVER,
            texture_pressed=TEX_RED_BUTTON_PRESS,
            style=button_style,
        )
        texture_button_with_icon_left.on_click = self.on_button_click
        grid.add(texture_button_with_icon_left, row=0, column=0)

        texture_button_with_icon_right = UITextureButton(
            text=questionList[self.random_int - 1][2],
            multiline=True,
            width=500,
            texture=TEX_RED_BUTTON_NORMAL,
            texture_hovered=TEX_RED_BUTTON_HOVER,
            texture_pressed=TEX_RED_BUTTON_PRESS,
            style=button_style,
        )
        texture_button_with_icon_right.on_click = self.on_button_click
        grid.add(texture_button_with_icon_right, row=0, column=1)

        texture_button_with_icon_left1 = UITextureButton(
            text=questionList[self.random_int - 1][3],
            multiline=True,
            width=500,
            texture=TEX_RED_BUTTON_NORMAL,
            texture_hovered=TEX_RED_BUTTON_HOVER,
            texture_pressed=TEX_RED_BUTTON_PRESS,
            style=button_style,
        )
        texture_button_with_icon_left1.on_click = self.on_button_click
        grid.add(texture_button_with_icon_left1, row=1, column=0)

        texture_button_with_icon_right1 = UITextureButton(
            text=questionList[self.random_int - 1][4],
            multiline=True,
            width=500,
            texture=TEX_RED_BUTTON_NORMAL,
            texture_hovered=TEX_RED_BUTTON_HOVER,
            texture_pressed=TEX_RED_BUTTON_PRESS,
            style=button_style,
        )
        texture_button_with_icon_right1.on_click = self.on_button_click
        grid.add(texture_button_with_icon_right1, row=1, column=1)

        # 3. Anchor the grid in the center of the screen and register it
        #    with the UI manager (UIView creates self.ui for you automatically)
        anchor = UIAnchorLayout()
        anchor.add(grid, anchor_x="center", anchor_y="center")
        self.ui.add(anchor)

    def on_button_click(self, event):
        """Called when the texture button is clicked."""
        answer_text = event.source.text
        correct_text = questionList[self.random_int - 1][5]

        if answer_text == correct_text:
            print("Correct answer!")
            speak_async(answer_text, "Correct!")
            battle = PlayScreen()
        else:
            print("Incorrect answer.")
            speak_async(answer_text, "Incorrect.")
            battle = PlayScreen()

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_draw(self):
        self.clear()
        #arcade.draw_texture_rect(self.background_texture, arcade.XYWH(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH-10, WINDOW_HEIGHT-10))
        self.player_list.draw()
        self.question_text.draw()
        # Explicitly draw the UI here. In newer Arcade, UIView auto-draws
        # self.ui after on_draw() returns, so this *could* double-draw —
        # but it won't cause errors, and it guarantees the UI shows up
        # even on Arcade versions where the auto-draw doesn't happen.
        self.ui.draw()

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

        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
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