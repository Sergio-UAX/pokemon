### main.py (PC-Only, v3.2 - Event-Driven Game Loop)
import sys
import json
import turtle
import os

# Import the "Brain"
from src.game import Game
from src.pokemon import Pokemon

# --- Screen Configuration ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# --- Global Turtles (Our "Pens") ---
screen = turtle.Screen()
player_turtle = turtle.Turtle()
opponent_turtle = turtle.Turtle()
ui_turtle = turtle.Turtle() # For writing text

# --- Global Game Engine (The "Brain") ---
game_engine = None
current_state = "" # Stores the game's current state

# --- Asset Loading ---

def load_pokemon_stats(pokemon_stats_json_path="data/pokemon_stats.json"):
    try:
        with open(pokemon_stats_json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: could not find {pokemon_stats_json_path}.")
        print(f"Please run 'tools/fetch_pokemon.py' first.")
        return None
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None

def register_sprites(pokemon_list):
    """Pre-loads all Pokémon sprites into Turtle's shapes."""
    for pokemon_data in pokemon_list:
        sprite_front = pokemon_data.get("sprite_front")
        sprite_back = pokemon_data.get("sprite_back")
        
        if sprite_front and os.path.exists(sprite_front):
            screen.register_shape(sprite_front)
        
        if sprite_back and os.path.exists(sprite_back):
            screen.register_shape(sprite_back)
    print("All sprites registered.")

# --- Drawing Functions (The "Face") ---

def setup_screen():
    """Creates and configures the main game window."""
    screen.title("Pokémon Battle Simulator")
    screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen.tracer(0) # Manual updates
    
    player_turtle.hideturtle()
    opponent_turtle.hideturtle()
    ui_turtle.hideturtle()
    
    player_turtle.penup()
    opponent_turtle.penup()
    ui_turtle.penup()

def draw_starter_selection():
    """Displays the starter selection text on the screen."""
    ui_turtle.clear()
    ui_turtle.goto(0, 100)
    ui_turtle.write("Choose your Pokémon!", align="center", font=("Arial", 24, "bold"))
    
    starter_names = game_engine.get_starter_info()
    ui_turtle.goto(0, 50)
    ui_turtle.write(f"Press '1' for {starter_names[0]}", align="center", font=("Arial", 16, "normal"))
    ui_turtle.goto(0, 20)
    ui_turtle.write(f"Press '2' for {starter_names[1]}", align="center", font=("Arial", 16, "normal"))
    ui_turtle.goto(0, -10)
    ui_turtle.write(f"Press '3' for {starter_names[2]}", align="center", font=("Arial", 16, "normal"))

def draw_battle_scene():
    """Draws the Pokémon sprites in their battle positions."""
    ui_turtle.clear() # Clear the selection text
    
    battle_info = game_engine.get_battle_info()
    if not battle_info: return 
        
    player_sprite = game_engine.player_pokemon.sprite_back
    opponent_sprite = game_engine.opponent_pokemon.sprite_front
    
    if player_sprite:
        player_turtle.shape(player_sprite)
        player_turtle.goto(-150, -100) # Player position
        player_turtle.showturtle()
        
    if opponent_sprite:
        opponent_turtle.shape(opponent_sprite)
        opponent_turtle.goto(150, 200) # Opponent position
        opponent_turtle.showturtle()
    
    print_battle_status_to_console()

def print_battle_status_to_console():
    """Prints battle info to the console (temporary)."""
    battle_info = game_engine.get_battle_info()
    if not battle_info:
        print("Waiting for battle to load...")
        return
        
    print("\n" + "="*30)
    print(f"  OPPONENT: {battle_info['opponent']['name']} (Lvl {battle_info['opponent']['level']})")
    print(f"  HP: {battle_info['opponent']['hp_actual']} / {battle_info['opponent']['hp_max']}")
    print("\n")
    print(f"  PLAYER: {battle_info['player']['name']} (Lvl {battle_info['player']['level']})")
    print(f"  HP: {battle_info['player']['hp_actual']} / {battle_info['player']['hp_max']}")
    print("="*30)
    
    print("Choose a move (Press 1, 2, 3, or 4 on keyboard):")
    for i, move in enumerate(battle_info['player']['moves']):
        print(f"  {i + 1}. {move['name']}")

# --- Input Functions (Connecting Keys to "Brain") ---

def select_starter_1():
    if game_engine.get_state() == 'STARTER_SELECTION':
        game_engine.select_starter(0) 
    
def select_starter_2():
    if game_engine.get_state() == 'STARTER_SELECTION':
        game_engine.select_starter(1) 

def select_starter_3():
    if game_engine.get_state() == 'STARTER_SELECTION':
        game_engine.select_starter(2) 

def select_move_1():
    if game_engine.get_state() == 'IN_BATTLE':
        game_engine.run_battle_turn(0) 
        print_battle_status_to_console()

def select_move_2():
    if game_engine.get_state() == 'IN_BATTLE':
        game_engine.run_battle_turn(1)
        print_battle_status_to_console()

def select_move_3():
    if game_engine.get_state() == 'IN_BATTLE':
        game_engine.run_battle_turn(2)
        print_battle_status_to_console()

def select_move_4():
    if game_engine.get_state() == 'IN_BATTLE':
        game_engine.run_battle_turn(3)
        print_battle_status_to_console()

def set_keybindings(state):
    """Activates and deactivates keys based on game state."""
    screen.listen() 
    
    if state == 'STARTER_SELECTION':
        screen.onkey(select_starter_1, "1")
        screen.onkey(select_starter_2, "2")
        screen.onkey(select_starter_3, "3")
        screen.onkey(None, "4") # Disable 4
    
    elif state == 'IN_BATTLE':
        screen.onkey(select_move_1, "1") 
        screen.onkey(select_move_2, "2")
        screen.onkey(select_move_3, "3")
        screen.onkey(select_move_4, "4") # Enable 4
    
    elif state == 'GAME_OVER':
        screen.onkey(None, "1")
        screen.onkey(None, "2")
        screen.onkey(None, "3")
        screen.onkey(None, "4")

# --- ¡NUEVO! Bucle de Juego Basado en Eventos ---

def game_loop():
    """
    This is the main game loop.
    It checks the state and draws the appropriate screen.
    """
    global current_state, game_engine
    
    # 1. Get the new state from the Brain
    new_state = game_engine.get_state()
    
    # 2. Check if the state changed
    if new_state != current_state:
        print(f"STATE CHANGE: {current_state} -> {new_state}")
        current_state = new_state
        
        # Re-bind keys for the new state
        set_keybindings(current_state)
        
        # Draw the correct screen for the new state
        if current_state == 'STARTER_SELECTION':
            draw_starter_selection()
        
        elif current_state == 'IN_BATTLE':
            draw_battle_scene()
        
        elif current_state == 'GAME_OVER':
            print("--- Game Over. Click window to exit. ---")
            screen.exitonclick()
            return # Stop the loop

    # 3. Process any messages from the Brain
    for message in game_engine.get_pending_messages():
        print(f"\n>> {message}")
    
    # 4. Update the Turtle screen
    screen.update()
    
    # 5. Schedule this function to run again
    # This is the magic that replaces "while running:"
    screen.ontimer(game_loop, 30) # ~33 frames per second

# --- Main Game Execution ---

if __name__ == "__main__":
    print("--- Starting Pokémon Simulator (PC Version) ---")
    
    setup_screen()
    
    pokemon_stats = load_pokemon_stats()
    
    if pokemon_stats:
        # 1. Initialize the Brain
        game_engine = Game(pokemon_stats)
        
        # 2. Register sprites
        register_sprites(pokemon_stats)
        
        # 3. Start the game loop
        game_loop()
        
        # 4. Tell Turtle to start its event loop
        # This will wait for key presses and run the ontimer
        turtle.done() 

    else:
        print("No se pudieron cargar los datos. Saliendo.")