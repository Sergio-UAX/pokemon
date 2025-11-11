""" LIBRARIES """
import requests # Connects to API
import json     # Creates .json
import os       # File manager

""" CONSTANTS """

# --- PATHS ---
# (Your logic for creating cross-platform paths)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
SPRITE_DIR = os.path.join(DATA_DIR, "sprites")
OUTPUT_FILE = os.path.join(DATA_DIR, "pokemon_stats.json")

# --- API VARIABLES ---
# We are still only fetching the starters for the MVP
STARTER_IDS = [1, 4, 7] # Bulbasaur, Charmander, Squirtle
BASE_API_URL = "https://pokeapi.co/api/v2/"

# --- DATA MAPPING ---
#
# *** THIS IS THE FIRST FIX ***
# Our src/pokemon.py expects the full, lowercase stat names.
# This map now ensures that's what we save.
# (e.g., API "special-attack" -> JSON "special-attack")
#
STAT_MAP = {
    "hp": "hp",
    "attack": "attack",
    "defense": "defense",
    "special-attack": "special-attack",
    "special-defense": "special-defense",
    "speed": "speed"
}

""" HELPER FUNCTIONS """

def get_move_data(move_url):
    """
    Fetches the details for a single move from its API URL.
    """
    try:
        response = requests.get(move_url)
        response.raise_for_status() # Check for errors
        move_data = response.json()
        
        # We will keep status moves (like Growl) for now
        # as they were in your original JSON.
        return {
            "name": move_data["name"].replace('-', ' ').capitalize(),
            "power": move_data["power"], # Will be None for status moves
            "type": move_data["type"]["name"].capitalize(),
            "category": move_data["damage_class"]["name"]
        }
    except requests.RequestException as e:
        print(f"Error fetching move data: {e}")
        return None

def download_sprite(url, save_path):
    """
    Downloads a file from a URL and saves it locally.
    """
    if not url:
        return None
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return save_path
    except requests.RequestException as e:
        print(f"Error downloading sprite: {e}")
        return None

""" PRIMARY FETCH FUNCTION """

def fetch_pokemon_data(pokemon_id):
    """
    Fetches all required data for a single Pokémon
    and formats it for our game.
    """
    try:
        print(f"\nFetching data for Pokémon ID: {pokemon_id}")
        pokemon_url = f"{BASE_API_URL}pokemon/{pokemon_id}"
        response = requests.get(pokemon_url)
        response.raise_for_status()
        pokemon_data = response.json()

        # Build the stats dictionary using our corrected STAT_MAP
        pokemon_stats = {}
        for stat_entry in pokemon_data["stats"]:
            api_name = stat_entry["stat"]["name"]
            if api_name in STAT_MAP:
                # Use the map to get the correct key (e.g., "special-attack")
                json_key = STAT_MAP[api_name]
                pokemon_stats[json_key] = stat_entry["base_stat"]
        
        # Get list of types
        types = [t["type"]["name"].capitalize() for t in pokemon_data["types"]]
        
        # Get move data
        print(f"Fetching move data for {pokemon_data['name']}...")
        moves = []
        for move_entry in pokemon_data["moves"]:
            # Filter for moves learned by leveling up
            if move_entry["version_group_details"][0]["move_learn_method"]["name"] == "level-up":
                move_url = move_entry["move"]["url"]
                move_data = get_move_data(move_url)
                if move_data:
                    moves.append(move_data)
                    if len(moves) >= 4: # Get 4 moves only
                        break
        
        # Get sprites
        print(f"Downloading sprites for {pokemon_data['name']}...")
        sprites_api = pokemon_data["sprites"]["versions"]["generation-v"]["black-white"]["animated"]
        
        # *** Preserving your custom sprite name format ***
        path_front = os.path.join(SPRITE_DIR, f"{pokemon_id}{pokemon_data['name']}_front.gif")
        path_back = os.path.join(SPRITE_DIR, f"{pokemon_id}{pokemon_data['name']}_back.gif")
        
        sprite_front_local = download_sprite(sprites_api["front_default"], path_front)
        sprite_back_local = download_sprite(sprites_api["back_default"], path_back)

        # Create the final, clean dictionary
        pokemon_clean = {
            "id": pokemon_id,
            "name": pokemon_data['name'].capitalize(),
            
            # *** THIS IS THE SECOND FIX ***
            # Renamed "types" (plural) to "type" (singular)
            # to match the _init_ of our Pokemon class.
            "type": types,
            
            "stats": pokemon_stats,
            "moves": moves,
            "sprite_front": sprite_front_local,
            "sprite_back": sprite_back_local
        }
        return pokemon_clean
        
    except requests.RequestException as e:
        print(f"Failed to fetch data for ID {pokemon_id}: {e}")
        return None

""" MAIN EXECUTION """

def main():
    """
    Main function to run the data fetching process.
    """
    # Create directories if they don't exist
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Path created: {DATA_DIR}")
    if not os.path.exists(SPRITE_DIR):
        os.makedirs(SPRITE_DIR)
        print(f"Path created: {SPRITE_DIR}")

    pokemon_list = []
    print("--- Starting Data Download ---")
    for poke_id in STARTER_IDS:
        data = fetch_pokemon_data(poke_id) 
        if data:
            pokemon_list.append(data)
        else:
            print(f"Could not get data for Pokémon ID: {poke_id}")

    # Save the data to the JSON file
    if pokemon_list:
        print(f"Saving final data to {OUTPUT_FILE}...")
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(pokemon_list, f, indent=4, ensure_ascii=False)
        print("Data downloaded successfully.")
    else:
        print("Could not get any data. No file was created.")

# Dunder check (con doble guion bajo, como pediste)
if __name__ == "__main__":
    main()