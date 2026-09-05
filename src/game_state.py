"""
Everything that needs to survive a view switch (PlayScreen <-> BattleScreen
<-> LearnScreen) lives here instead of being passed through every __init__.
Because Python only imports a module once, `state` below is a singleton --
every file that does `from game_state import state` shares the exact same
object, so e.g. coins collected in PlayScreen are still there when you open
the Shop, and power-ups bought in the Shop still apply in Battle.
"""

DEFAULT_TEXT_SCALE = 1.0
MIN_TEXT_SCALE = 0.75
MAX_TEXT_SCALE = 1.75

DEFAULT_MUSIC_VOLUME = 0.5


# Power-up catalog: id -> definition. `effect_per_level` is added up for
# every level currently owned (see GameState.power_up_value).
POWER_UP_DEFS = {
    "speed": {
        "name": "Speed Boost",
        "description": "Move faster around the map.",
        "base_cost": 30,
        "cost_growth": 1.6,
        "max_level": 3,
        "effect_per_level": 1.5,
    },
    "damage": {
        "name": "Power Strike",
        "description": "Deal extra damage per correct answer.",
        "base_cost": 40,
        "cost_growth": 1.6,
        "max_level": 3,
        "effect_per_level": 5,
    },
    "coin_boost": {
        "name": "Coin Magnet",
        "description": "Earn extra coins from every pickup.",
        "base_cost": 35,
        "cost_growth": 1.6,
        "max_level": 3,
        "effect_per_level": 5,
    },
}


class GameState:
    """Holds currency, settings, and power-up levels for the whole game."""

    def __init__(self):
        self.currency = 0
        self.text_scale = DEFAULT_TEXT_SCALE

        self.music_enabled = True
        self.music_volume = DEFAULT_MUSIC_VOLUME

        # power_id -> current level (0 = not purchased yet)
        self.power_up_levels = {power_id: 0 for power_id in POWER_UP_DEFS}

    # ---------------------------------------------------------- currency --
    def add_currency(self, amount):
        self.currency = max(0, self.currency + amount)

    def can_afford(self, amount):
        return self.currency >= amount

    def spend(self, amount):
        if not self.can_afford(amount):
            return False
        self.currency -= amount
        return True

    # -------------------------------------------------------- text scale --
    def set_text_scale(self, value):
        self.text_scale = max(MIN_TEXT_SCALE, min(MAX_TEXT_SCALE, value))

    def scaled(self, base_size):
        """base_size * current text_scale, rounded to a usable int font size."""
        return max(1, round(base_size * self.text_scale))

    # -------------------------------------------------------- power-ups --
    def power_up_cost(self, power_id):
        """Cost to buy the NEXT level of a power-up, or None if maxed out."""
        info = POWER_UP_DEFS[power_id]
        level = self.power_up_levels[power_id]
        if level >= info["max_level"]:
            return None
        return round(info["base_cost"] * (info["cost_growth"] ** level))

    def buy_power_up(self, power_id):
        """Attempt to purchase the next level. Returns (success, message)."""
        cost = self.power_up_cost(power_id)
        if cost is None:
            return False, "Already maxed out!"
        if not self.spend(cost):
            return False, "Not enough coins!"
        self.power_up_levels[power_id] += 1
        return True, f"{POWER_UP_DEFS[power_id]['name']} upgraded!"

    def power_up_value(self, power_id):
        """Total bonus currently granted by a power-up, across every level bought."""
        info = POWER_UP_DEFS[power_id]
        return info["effect_per_level"] * self.power_up_levels[power_id]

    @property
    def speed_bonus(self):
        return self.power_up_value("speed")

    @property
    def damage_bonus(self):
        return self.power_up_value("damage")

    @property
    def coin_bonus(self):
        return self.power_up_value("coin_boost")


# The single shared instance -- import THIS, not the class.
state = GameState()
