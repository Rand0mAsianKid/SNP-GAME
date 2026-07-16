import arcade


class Battle(arcade.View):

    def __init__(self):
        super().__init__()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_RED)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "BATTLE SCREEN",
            500,
            350,
            arcade.color.WHITE,
            40
        )

    def on_update(self, delta_time):
        pass