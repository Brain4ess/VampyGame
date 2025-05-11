# name: Code name of the ability
# display_name: Display name of the ability
# icon: Path to the icon of the ability that appears in the upgrade menu
# sprite: Path to the sprites of the ability that appears in the game
# sound: Path to the sound of the ability (It sounds when the ability hits the enemy)

ABILITIES: dict = {
    
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
    "homing shot": {
        'name': 'homing shot',
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
    "lightning strike": {
        'name': 'lightning strike',
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

# All passive abilities have '[•]' in their names
PASSIVES: dict = {
    'duplicator': {  # +1 to projectiles per level for each ability a player has
        'name': 'duplicator',
        'display_name': 'Duplicator [•]',
        'icon': 'assets/images/abilities/passives/duplicator/icon.png',
        'max_level': 3,
        'class': 'Duplicator'
    },
    
    'overclock': {  # Reduces the cooldowns of all abilities
        'name': 'overclock',
        'display_name': 'Overclock [•]',
        'icon': 'assets/images/abilities/passives/overclock/icon.png',
        'max_level': 3,
        'class': 'Overclock'
    },
    
    'mirror': { # Clones random active ability
        'name': 'mirror',
        'display_name': 'Mirror [•]',
        'icon': 'assets/images/abilities/passives/mirror/icon.png',
        'max_level': 5,
        'class': 'Mirror'
    },
    
    'overlevel':{  # +1 to max_level to all abilities except self and rare passives
        'name': 'overlevel',
        'display_name': 'Overlevel [•]',
        'icon': 'assets/images/abilities/passives/overlevel/icon.webp',
        'max_level': 1,
        'class': 'Overlevel'
    },
    
    'moreExp': {  # Gives you more experience from killing enemies
        'name': 'moreExp',
        'display_name': 'More Experience [•]',
        'icon': 'assets/images/abilities/passives/more experience/icon.png',
        'max_level': 3,
        'class': 'MoreExp'
    },
    
    'cheese': {  # Allows you to respawn once after death
        'name': 'cheese',
        'display_name': 'Cheese [•]',
        'icon': 'assets/images/abilities/passives/cheese/icon.png',
        'max_level': 1,
        'class': 'Cheese'
    }
}
