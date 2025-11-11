### src/utils.py (NEW FILE)
# This file holds utility functions and constant data,
# like the Type Chart.

# --- TYPE CHART ---
# Key: Attacking Type
# Value: Dictionary of {Defending Type: Multiplier}
TYPE_CHART = {
    "Normal": {
        "Rock": 0.5, "Ghost": 0.0, "Steel": 0.5
    },
    "Fire": {
        "Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 2.0, 
        "Bug": 2.0, "Rock": 0.5, "Dragon": 0.5, "Steel": 2.0
    },
    "Water": {
        "Fire": 2.0, "Water": 0.5, "Grass": 0.5, "Ground": 2.0, 
        "Rock": 2.0, "Dragon": 0.5
    },
    "Grass": {
        "Fire": 0.5, "Water": 2.0, "Grass": 0.5, "Poison": 0.5, 
        "Ground": 2.0, "Flying": 0.5, "Bug": 0.5, "Rock": 2.0, 
        "Dragon": 0.5, "Steel": 0.5
    },
    "Electric": {
        "Water": 2.0, "Grass": 0.5, "Ground": 0.0, "Flying": 2.0, 
        "Dragon": 0.5
    },
    "Ice": {
        "Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ground": 2.0, 
        "Flying": 2.0, "Dragon": 2.0, "Steel": 0.5, "Ice": 0.5
    },
    "Fighting": {
        "Normal": 2.0, "Ice": 2.0, "Poison": 0.5, "Flying": 0.5, 
        "Psychic": 0.5, "Bug": 0.5, "Rock": 2.0, "Ghost": 0.0, 
        "Dark": 2.0, "Steel": 2.0, "Fairy": 0.5
    },
    "Poison": {
        "Grass": 2.0, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, 
        "Ghost": 0.5, "Steel": 0.0, "Fairy": 2.0
    },
    "Ground": {
        "Fire": 2.0, "Electric": 2.0, "Grass": 0.5, "Poison": 2.0, 
        "Flying": 0.0, "Bug": 0.5, "Rock": 2.0, "Steel": 2.0
    },
    "Flying": {
        "Electric": 0.5, "Grass": 2.0, "Fighting": 2.0, "Bug": 2.0, 
        "Rock": 0.5, "Steel": 0.5
    },
    "Psychic": {
        "Fighting": 2.0, "Poison": 2.0, "Psychic": 0.5, "Dark": 0.0, 
        "Steel": 0.5
    },
    "Bug": {
        "Fire": 0.5, "Grass": 2.0, "Fighting": 0.5, "Poison": 0.5, 
        "Flying": 0.5, "Psychic": 2.0, "Ghost": 0.5, "Dark": 2.0, 
        "Steel": 0.5, "Fairy": 0.5
    },
    "Rock": {
        "Fire": 2.0, "Ice": 2.0, "Fighting": 0.5, "Ground": 0.5, 
        "Flying": 2.0, "Bug": 2.0, "Steel": 0.5
    },
    "Ghost": {
        "Normal": 0.0, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5
    },
    "Dragon": {
        "Dragon": 2.0, "Steel": 0.5, "Fairy": 0.0
    },
    "Dark": {
        "Fighting": 0.5, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5, 
        "Fairy": 0.5
    },
    "Steel": {
        "Ice": 2.0, "Rock": 2.0, "Fairy": 2.0, "Fire": 0.5, 
        "Water": 0.5, "Electric": 0.5, "Steel": 0.5
    },
    "Fairy": {
        "Fighting": 2.0, "Poison": 0.5, "Dragon": 2.0, 
        "Dark": 2.0, "Steel": 0.5
    }
}


def get_type_effectiveness(move_type, defender_types):
    """
    Calculates the type effectiveness multiplier.
    """
    if move_type not in TYPE_CHART:
        return 1.0 

    total_multiplier = 1.0
    move_effectiveness = TYPE_CHART.get(move_type, {})
    
    for def_type in defender_types:
        multiplier = move_effectiveness.get(def_type, 1.0)
        total_multiplier *= multiplier
        
    return total_multiplier