# image_multiplier: Number that determine the size increase of enemy sprites (Default: 1)
# sound: The sound that will be played when an enemy is hit (Default: None)
# weight: The number responsible for the frequency of enemy appearances (more means more often)
# exp: The amount of exp the player gets for killing an enemy

ENEMIES: dict = {
    'onre': {
        'sprites': 'assets/enemies/onre',
        'image_multiplier': 1,
        'health': 30,
        'damage': 2,
        'speed': 4,
        'sound': 'assets/sounds/SFX/ButtonClick1.wav',
        'weight': 30,
        'exp': 10
    },
    
    'orcShaman': {
        'sprites': 'assets/enemies/orcShaman',
        'image_multiplier': 1,
        'health': 60,
        'damage': 3,
        'speed': 3.5,
        'sound': 'assets/sounds/SFX/ButtonClick1.wav',
        'weight': 10,
        'exp': 20
    },
    
    'orcWarrior': {
        'sprites': 'assets/enemies/orcWarrior',
        'image_multiplier': 1,
        'health': 60,
        'damage': 3,
        'speed': 3.5,
        'sound': 'assets/sounds/SFX/ButtonClick1.wav',
        'weight': 20,
        'exp': 15
    }
}
