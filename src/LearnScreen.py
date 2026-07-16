"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import random
import math

import arcade

import pyttsx3
import threading

from PIL import Image, ImageDraw, ImageFilter

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
from arcade.gui.property import bind
from matplotlib.pylab import matrix

import PlayScreen

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Starting Template"

engine1 = pyttsx3.init()

speech_lock = threading.Lock()


def speak_async(*phrases):
    engine1.stop() 

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
    FONT_NAME = ("arial", "calibri")
    FONT_NAME_BOLD = ("arial", "calibri")

QUESTION_FONT_SIZE = 40
BUTTON_FONT_SIZE = 21          
BUTTON_FONT_MIN_SIZE = 13      
BUTTON_TEXT_H_MARGIN = 90
BUTTON_TEXT_V_MARGIN = 18

TITLE_COLOR_1 = (224, 122, 100)
TITLE_COLOR_2 = (40, 66, 102)
BUTTON_TEXT_COLOR = (58, 50, 44)

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



# ---------------------------------------------------------------------------
def make_background(width, height, seed=7):
    """Warm cream background with a soft pastel rainbow swipe and bokeh dots."""

    rng = random.Random(seed)
    img = Image.new("RGB", (width, height), (247, 238, 222))
    draw = ImageDraw.Draw(img, "RGBA")

    band_colors = [
        (240, 170, 150, 55),
        (245, 205, 150, 55),
        (240, 230, 160, 55),
        (190, 220, 190, 55),
        (175, 205, 225, 55),
        (195, 190, 220, 55),
    ]
    cx, cy = width * 0.52, height * 0.52
    length = width * 0.9
    for i, color in enumerate(band_colors):
        off = (i - len(band_colors) / 2) * 22
        x1 = cx - length / 2 + off
        y1 = cy + length * 0.28 - off * 0.25
        x2 = cx + length / 2 + off
        y2 = cy - length * 0.28 - off * 0.25
        draw.line([(x1, y1), (x2, y2)], fill=color, width=34)

    img = img.filter(ImageFilter.GaussianBlur(35))
    draw = ImageDraw.Draw(img, "RGBA")

    for _ in range(55):
        x = rng.randint(0, width)
        y = rng.randint(0, height)
        r = rng.randint(3, 16)
        alpha = rng.randint(12, 55)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, alpha))

    star_colors = [(120, 150, 190, 180), (230, 150, 140, 180), (210, 190, 120, 180)]
    for _ in range(14):
        x = rng.randint(0, width)
        y = rng.randint(0, height)
        r = rng.randint(3, 6)
        col = rng.choice(star_colors)
        pts = []
        for k in range(4):
            ang = k * math.pi / 2
            pts.append((x + r * math.cos(ang), y + r * math.sin(ang)))
            ang2 = ang + math.pi / 4
            pts.append((x + r * 0.35 * math.cos(ang2), y + r * 0.35 * math.sin(ang2)))
        draw.polygon(pts, fill=col)

    return img.convert("RGBA")


def make_pill(width, height, base_color, pad=18, shadow_offset=6, shadow_blur=10,
              top_light=22, bottom_dark=22, border_light=90):

    pad = max(pad, shadow_offset + shadow_blur * 3 + 6)
    img = Image.new("RGBA", (width + pad * 2, height + pad * 2), (0, 0, 0, 0))
    radius = height // 2

    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle(
        [pad, pad + shadow_offset, pad + width, pad + height + shadow_offset],
        radius=radius, fill=(60, 50, 40, 95),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(shadow_blur))
    img = Image.alpha_composite(img, shadow)

    fill_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(fill_layer)
    top = tuple(min(255, c + top_light) for c in base_color)
    bottom = tuple(max(0, c - bottom_dark) for c in base_color)
    for y in range(height):
        t = y / height
        r = int(top[0] * (1 - t) + bottom[0] * t)
        g = int(top[1] * (1 - t) + bottom[1] * t)
        b = int(top[2] * (1 - t) + bottom[2] * t)
        fdraw.line([(pad, pad + y), (pad + width, pad + y)], fill=(r, g, b, 255))

    mask = Image.new("L", img.size, 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([pad, pad, pad + width - 1, pad + height - 1], radius=radius, fill=255)
    img.paste(fill_layer, (0, 0), mask)

    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [pad, pad, pad + width - 1, pad + height - 1],
        radius=radius, outline=(70, 62, 55, 140), width=2,
    )
    inset = 5
    draw.arc(
        [pad + inset, pad + inset, pad + width - inset, pad + height - inset + 20],
        start=200, end=340, fill=(255, 255, 255, border_light), width=3,
    )

    return img


def make_glow(width, height, color=(255, 250, 235, 190), blur=18, radius=40):
    """A soft blurred halo, sized to sit behind the question title so the
    text pops off the background like in the reference image."""
    pad = blur * 2
    img = Image.new("RGBA", (int(width) + pad * 2, int(height) + pad * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([pad, pad, pad + width, pad + height], radius=radius, fill=color)
    return img.filter(ImageFilter.GaussianBlur(blur))


def fit_font_size(text, max_width, max_height, font_name,
                   start_size=BUTTON_FONT_SIZE, min_size=BUTTON_FONT_MIN_SIZE):
    """Shrink font_size (from start_size down to min_size) until the wrapped
    text fits within max_width x max_height. Uses the same probe-Text trick
    already used for measuring the title, so long answers on the smaller
    buttons don't overflow the pill."""
    size = start_size
    while size > min_size:
        probe = arcade.Text(
            text, x=0, y=0, font_size=size, font_name=font_name,
            multiline=True, width=max_width, bold=True,
        )
        if probe.content_height <= max_height:
            return size
        size -= 1
    return min_size


BACKGROUND_TEXTURE = arcade.Texture(make_background(WINDOW_WIDTH, WINDOW_HEIGHT))

BUTTON_CONTENT_WIDTH = 500
BUTTON_CONTENT_HEIGHT = 110
BUTTON_BASE_COLOR = (176, 170, 163)

BUTTON_TEXTURE_PAD = 50

BTN_TEXTURE_NORMAL = arcade.Texture(
    make_pill(BUTTON_CONTENT_WIDTH, BUTTON_CONTENT_HEIGHT, BUTTON_BASE_COLOR,
              pad=BUTTON_TEXTURE_PAD, shadow_offset=6, shadow_blur=10)
)
BTN_TEXTURE_HOVER = arcade.Texture(
    make_pill(BUTTON_CONTENT_WIDTH, BUTTON_CONTENT_HEIGHT,
              tuple(min(255, c + 10) for c in BUTTON_BASE_COLOR),
              pad=BUTTON_TEXTURE_PAD, shadow_offset=8, shadow_blur=12)
)
BTN_TEXTURE_PRESSED = arcade.Texture(
    make_pill(BUTTON_CONTENT_WIDTH, BUTTON_CONTENT_HEIGHT,
              tuple(max(0, c - 14) for c in BUTTON_BASE_COLOR),
              pad=BUTTON_TEXTURE_PAD, shadow_offset=2, shadow_blur=6)
)


class GameView(UIView):

    def __init__(self):
        super().__init__()
        self.random_int = random.randint(1, 5)


        self.background_color = (247, 238, 222)

        # 1. Create a container to hold your sprites
        self.player_list = arcade.SpriteList()

        question = questionList[self.random_int - 1][0]


        split_at = len(question) // 2
        space_idx = question.find(" ", split_at)
        if space_idx == -1:
            space_idx = split_at
        part1 = question[:space_idx + 1]
        part2 = question[space_idx + 1:]

        title_y = WINDOW_HEIGHT - 70

        probe1 = arcade.Text(part1, x=0, y=title_y, font_size=QUESTION_FONT_SIZE,
                              font_name=FONT_NAME_BOLD, bold=True)
        probe2 = arcade.Text(part2, x=0, y=title_y, font_size=QUESTION_FONT_SIZE,
                              font_name=FONT_NAME_BOLD, bold=True)
        total_width = probe1.content_width + probe2.content_width
        start_x = WINDOW_WIDTH / 2 - total_width / 2

        self.title_text_1 = arcade.Text(
            part1, x=start_x, y=title_y, color=TITLE_COLOR_1,
            font_size=QUESTION_FONT_SIZE, font_name=FONT_NAME_BOLD, bold=True,
            anchor_x="left", anchor_y="center",
        )
        self.title_text_2 = arcade.Text(
            part2, x=start_x + probe1.content_width, y=title_y, color=TITLE_COLOR_2,
            font_size=QUESTION_FONT_SIZE, font_name=FONT_NAME_BOLD, bold=True,
            anchor_x="left", anchor_y="center",
        )

        glow_image = make_glow(total_width + 20, probe1.content_height + 10)
        self.title_glow = arcade.Sprite(arcade.Texture(glow_image))
        self.title_glow.center_x = WINDOW_WIDTH / 2
        self.title_glow.center_y = title_y
        self.decor_sprite_list = arcade.SpriteList()
        self.decor_sprite_list.append(self.title_glow)

        speak_async(question)

        grid = UIGridLayout(
            column_count=2,
            row_count=2,
            size_hint=(0, 0),
            vertical_spacing=36,
            horizontal_spacing=60,
        )

        text_max_width = BUTTON_CONTENT_WIDTH - BUTTON_TEXT_H_MARGIN
        text_max_height = BUTTON_CONTENT_HEIGHT - BUTTON_TEXT_V_MARGIN

        answers = [
            questionList[self.random_int - 1][1],
            questionList[self.random_int - 1][2],
            questionList[self.random_int - 1][3],
            questionList[self.random_int - 1][4],
        ]

        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]

        for answer_text, (row, col) in zip(answers, positions):
            fitted_size = fit_font_size(
                answer_text, text_max_width, text_max_height, FONT_NAME_BOLD
            )

            button_style = {
                "normal": UITextureButton.UIStyle(
                    font_size=fitted_size,
                    font_name=FONT_NAME_BOLD,
                    font_color=BUTTON_TEXT_COLOR,
                ),
                "hover": UITextureButton.UIStyle(
                    font_size=fitted_size,
                    font_name=FONT_NAME_BOLD,
                    font_color=BUTTON_TEXT_COLOR,
                ),
                "press": UITextureButton.UIStyle(
                    font_size=fitted_size,
                    font_name=FONT_NAME_BOLD,
                    font_color=(255, 255, 255),
                ),
                "disabled": UITextureButton.UIStyle(
                    font_size=fitted_size,
                    font_name=FONT_NAME_BOLD,
                    font_color=(150, 145, 140),
                ),
            }

            texture_button = UITextureButton(
                text=answer_text,
                multiline=True,
                width=BTN_TEXTURE_NORMAL.width,
                height=BTN_TEXTURE_NORMAL.height,
                texture=BTN_TEXTURE_NORMAL,
                texture_hovered=BTN_TEXTURE_HOVER,
                texture_pressed=BTN_TEXTURE_PRESSED,
                style=button_style,
            )
            texture_button.on_click = self.on_button_click

            texture_button.place_text(
                anchor_x="center", align_x=0,
                anchor_y="center", align_y=0,
            )

            ui_label = getattr(texture_button, "ui_label", None)
            if ui_label is not None:
                try:
                    ui_label.align = "center"
                    ui_label.anchor_x = "center"
                except AttributeError:
                    pass

            bind(texture_button, "hovered", texture_button.trigger_full_render)
            bind(texture_button, "pressed", texture_button.trigger_full_render)
            texture_button.trigger_full_render()
            grid.add(texture_button, row=row, column=col)


        anchor = UIAnchorLayout()
        anchor.add(grid, anchor_x="center", anchor_y="center", align_y=-40)
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
        pass

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            BACKGROUND_TEXTURE,
            arcade.XYWH(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT),
        )

        self.decor_sprite_list.draw()
        self.player_list.draw()
        self.title_text_1.draw()
        self.title_text_2.draw()
        self.ui.draw()

    def on_update(self, delta_time):

        self.player_list.update()

    def on_key_press(self, key, key_modifiers):


        pass

    def on_key_release(self, key, key_modifiers):
 
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):

        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
 
        #play_screen = PlayScreen.PlayScreen()   # or PlayScreen.GameView()
        #self.window.show_view(play_screen)
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
    
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