### src/game.py (The Main "Brain")
import random
from .pokemon import Pokemon
from .battle import Battle

class Game:
    """
    The main "Brain" of the game. Manages state
    (menus, battle, etc.) and logic. It is 100% pure.
    """
    def __init__(self, pokemon_stats):
        self.pokemon_stats = pokemon_stats
        self.state = 'STARTER_SELECTION' # State machine
        self.pending_messages = []
        
        self.player_pokemon = None
        self.opponent_pokemon = None
        self.current_battle = None

    # --- Functions for main.py (The "Face") ---
    
    def get_state(self):
        """Returns the current game state."""
        return self.state

    def get_pending_messages(self):
        """Returns the message queue and clears it."""
        messages = self.pending_messages
        self.pending_messages = []
        return messages

    def get_starter_info(self):
        """Returns a list of starter names."""
        return [s['name'] for s in self.pokemon_stats]

    def get_battle_info(self):
        """Returns a dictionary with the current battle state."""
        if self.current_battle:
            return self.current_battle.get_state_info()
        return None

    # --- Logic Functions (Mutations) ---

    def select_starter(self, chosen_index):
        """Logic for when the player selects a starter."""
        # 1. Create the player's Pokémon
        player_data = self.pokemon_stats[chosen_index]
        self.player_pokemon = Pokemon(**player_data)
        self.log(f"You chose {self.player_pokemon.name}!")
        
        # 2. The opponent chooses another
        possible_indices = [0, 1, 2]
        possible_indices.pop(chosen_index)
        opponent_index = random.choice(possible_indices)
        
        opponent_data = self.pokemon_stats[opponent_index]
        self.opponent_pokemon = Pokemon(**opponent_data)
        self.log(f"Your opponent chose {self.opponent_pokemon.name}!")
        
        # 3. Start the battle
        self.current_battle = Battle(self.player_pokemon, self.opponent_pokemon, self.log)
        self.state = 'IN_BATTLE'

    def run_battle_turn(self, player_move_index):
        """Executes one full battle turn."""
        if not self.current_battle:
            return
            
        player_move = self.player_pokemon.moves[player_move_index]
        opponent_move = random.choice(self.opponent_pokemon.moves)
        
        # (We assume player is faster for now)
        # TODO: Implement speed check
        self.current_battle.execute_action(self.player_pokemon, self.opponent_pokemon, player_move)
        
        if self.opponent_pokemon.is_alive():
            self.current_battle.execute_action(self.opponent_pokemon, self.player_pokemon, opponent_move)

        # Check for end-of-battle conditions
        if not self.player_pokemon.is_alive():
            self.log(f"You have been defeated!")
            self.state = 'GAME_OVER'
        elif not self.opponent_pokemon.is_alive():
            self.log(f"You won!")
            self.state = 'GAME_OVER'

    def log(self, message):
        """Adds a message to the queue for the "Face" (main.py) to display."""
        self.pending_messages.append(message)