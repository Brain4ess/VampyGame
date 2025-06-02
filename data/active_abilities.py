'''A module that stores active abilities data'''
# name: Code name of the ability
# display_name: Display name of the ability
# icon: Path to the icon of the ability that appears in the upgrade menu
# sprite: Path to the sprites of the ability that appears in the game
# sound: Path to the sound of the ability (It sounds when the ability hits the enemy)

ACTIVE_ABILITIES: dict = {

    # Fires a shuriken that flies into a random enemy position
    "shuriken": {
        'name': 'shuriken',
        'display_name': 'Shuriken',
        'icon': 'assets/images/abilities/active_abilities/shuriken/Shuriken.png',
        'sprite': 'assets/images/abilities/active_abilities/shuriken/Shuriken.png',
        'speed': 7,
        'class': 'Shuriken',
        'sound': None,
        'damage': 7,
        'lifetime': 2,
        'cooldown': 2,
        'max_level': 5
    },

    # Launches a homing shot that flies until it reaches its target (if the target is gone, it flies to the point where it died and then disappears)
    "homing_shot": {
        'name': 'homing_shot',
        'display_name': 'Homing Shot',
        'icon': 'assets/images/abilities/active_abilities/HomingShot/1.png',
        'sprite': 'assets/images/abilities/active_abilities/HomingShot',
        'speed': 4,
        'class': 'HomingShot',
        'sound': None,
        'damage': 100,
        'lifetime': 2,
        'cooldown': 4,
        'max_level': 5,
        'hp': 1
    },

    # Unleashes a lightning strike that attacks multiple targets with a slight delay
    "lightning_strike": {
        'name': 'lightning_strike',
        'display_name': 'Lightning Strike',
        'icon': 'assets/images/abilities/active_abilities/LightningStrike/2.png',
        'sprite': 'assets/images/abilities/active_abilities/LightningStrike',
        'speed': 0,
        'class': 'LightningStrike',
        'sound': 'assets/sounds/abilities/LightningStrike/strike.wav',
        'random-sounds-dir': 'assets/sounds/abilities/LightningStrike/buildup',
        'damage': 25,
        'lifetime': 0,
        'cooldown': 60,
        'max_level': 5,
        'max_enemies': 3
    },

    # Starburst a specific enemy
    "starfall": {
        'name': 'starfall',
        'display_name': 'Starfall',
        'icon': 'assets/images/abilities/active_abilities/Starfall/9.png',
        'sprite': 'assets/images/abilities/active_abilities/Starfall',
        'speed': 7,
        'class': 'Starfall',
        'sound': None,
        'damage': 100,
        'lifetime': 0,
        'cooldown': 5,
        'max_level': 5
    },

    # Slash attack that pushes enemies around, also increases the number of slashes depending on the passive ability 'Duplicator' pumping
    "slash": {
        'name': 'slash',
        'display_name': 'Slash',
        'icon': 'assets/images/abilities/active_abilities/slash/green/6.png',
        'sprites': {
            'green': 'assets/images/abilities/active_abilities/slash/green',
            'red': 'assets/images/abilities/active_abilities/slash/red',
            'cyan': 'assets/images/abilities/active_abilities/slash/cyan',
            'orange': 'assets/images/abilities/active_abilities/slash/orange',
            'blue': 'assets/images/abilities/active_abilities/slash/blue'
            },
        'speed': 0,
        'class': 'Slash',
        'sound': None,
        'damage': 10,
        'lifetime': 0,
        'cooldown': 10,
        'max_level': 5
    }
}
