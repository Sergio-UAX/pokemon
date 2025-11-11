### src/pokemon.py (The Pokémon Template)

class Pokemon:
    """
    Defines a static Pokémon for battle (Level 5, no progression).
    """
    def __init__(self, name, type, stats, moves, 
                 sprite_front, sprite_back, id=None, **kwargs):
        
        self.name = name
        self.type = type # (e.g. ["Plant", "Poison"])
        self.moves = moves # (e.g. [{"name": "Tackle", "power": 40, ...}, ...])
        self.sprite_front = sprite_front
        self.sprite_back = sprite_back
        self.id = id
        
        # Fixed Level 5 as requested
        self.level = 5
        
        # Base stats (from JSON)
        self._base_stats = stats
        
        # Actual stats (calculated for Lvl 5)
        self.stats = {}
        self.hp_max = self._calculate_stat('hp')
        self.hp_actual = self.hp_max
        
        # Pre-calculate other stats
        self.stats['attack'] = self._calculate_stat('attack')
        self.stats['defense'] = self._calculate_stat('defense')
        self.stats['special-attack'] = self._calculate_stat('special-attack')
        self.stats['special-defense'] = self._calculate_stat('special-defense')
        self.stats['speed'] = self._calculate_stat('speed')

    def _calculate_stat(self, stat_name):
        """Calculates a stat based on Level 5 (Simple formula, no EVs/IVs)."""
        base_val = self._base_stats.get(stat_name, 10)
        
        if stat_name == 'hp':
            # HP Formula
            return int(((2 * base_val) * self.level / 100) + self.level + 10)
        else:
            # General Formula
            return int(((2 * base_val) * self.level / 100) + 5)

    def take_damage(self, damage):
        """Subtracts damage from current HP."""
        self.hp_actual -= damage
        if self.hp_actual < 0:
            self.hp_actual = 0

    def is_alive(self):
        """Checks if the Pokémon has HP greater than 0."""
        return self.hp_actual > 0
        
    def get_simple_info(self):
        """Returns a dict for the "Face" (main.py) to use."""
        return {
            "name": self.name,
            "level": self.level,
            "hp_actual": self.hp_actual,
            "hp_max": self.hp_max,
            "moves": self.moves
        }

    def to_dict(self):
        """Converts the Pokémon's state to a dictionary for saving."""
        # (We will use this later if we add a save/load feature)
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "hp_actual": self.hp_actual
        }