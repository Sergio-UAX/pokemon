### src/battle.py (The Battle "Brain" - NOW WITH REAL LOGIC)
import random
from . import utils # <-- Importa la tabla de tipos

class Battle:
    """
    Manages the pure logic of a battle turn.
    Knows nothing about "print" or "input".
    """
    def _init_(self, player_pokemon, opponent_pokemon, logger_callback):
        # Este _init_ SÍ acepta argumentos
        self.player_pokemon = player_pokemon
        self.opponent_pokemon = opponent_pokemon
        self.log = logger_callback # A function (like Game.log) to send messages

    def _calculate_damage(self, attacker, defender, move):
        """
        Calculates the damage of a move using the real
        Gen 1-5 damage formula.
        """
        
        # --- 1. Check for Status Move ---
        if move['power'] is None:
            return 0, 1.0 # Return 0 damage

        # --- 2. Get Stats (Physical vs Special) ---
        if move['category'] == 'physical':
            attack_stat = attacker.stats['attack']
            defense_stat = defender.stats['defense']
        else: # 'special'
            attack_stat = attacker.stats['special-attack']
            defense_stat = defender.stats['special-defense']
            
        # --- 3. Core Formula ---
        level = attacker.level
        power = move['power']
        damage = (((2 * level / 5 + 2) * power * attack_stat / defense_stat) / 50) + 2

        # --- 4. Modifiers (STAB & Type) ---
        stab_multiplier = 1.0
        if move['type'] in attacker.type:
            stab_multiplier = 1.5
            
        type_multiplier = utils.get_type_effectiveness(move['type'], defender.type)
        
        # --- 5. Randomness ---
        random_multiplier = random.uniform(0.85, 1.0)
        
        # --- 6. Final Damage ---
        final_damage = damage * stab_multiplier * type_multiplier * random_multiplier
        
        return int(final_damage), type_multiplier

    def execute_action(self, attacker, defender, move):
        """Executes a single attack action."""
        
        self.log(f"{attacker.name} used {move['name']}!")
        
        damage, type_multiplier = self._calculate_damage(attacker, defender, move)
        
        if damage > 0:
            if type_multiplier > 1.0:
                self.log("It's super effective!")
            elif type_multiplier < 1.0 and type_multiplier > 0.0:
                self.log("It's not very effective...")
            elif type_multiplier == 0.0:
                self.log(f"It doesn't affect {defender.name}...")

            self.log(f"It deals {damage} damage!")
            defender.take_damage(damage)
        else:
            self.log("But it failed!") # (Simple log for status moves)
            
        self.log(f"{defender.name} has {defender.hp_actual}/{defender.hp_max} HP remaining.")

    def get_state_info(self):
        """Returns a dictionary with info for the "Face" (main.py)."""
        return {
            "player": self.player_pokemon.get_simple_info(),
            "opponent": self.opponent_pokemon.get_simple_info()
        }