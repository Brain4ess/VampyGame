
ABILITIES: dict = {
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
    
    "starfall": {
        'name': 'starfall',
        'display_name': 'Starfall',
        'icon': 'assets/images/abilities/active_abilities/Starfall/9.png',
        'sprite': 'assets/images/abilities/active_abilities/Starfall',
        'speed': 7,
        'class': 'Starfall',
        'sound': None,
        'damage': 10,
        'lifetime': 0,
        'cooldown': 5,
        'max_level': 5
    },
    
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


PASSIVES: dict = {
    'duplicator': {  # +1 proj every level to every ability a player has
        'name': 'duplicator',
        'display_name': 'Duplicator [•]',
        'icon': 'assets/images/abilities/passives/duplicator/icon.png',
        'max_level': 3,
        'class': 'Duplicator'
    },
    
    'overclock': {  # cooldown decreaser for all abilities
        'name': 'overclock',
        'display_name': 'Overclock [•]',
        'icon': 'assets/images/abilities/passives/overclock/icon.png',
        'max_level': 3,
        'class': 'Overclock'
    },
    
    'mirror': { # clones (random?) active ability, maybe more rare to get this?
        'name': 'mirror',
        'display_name': 'Mirror [•]',
        'icon': 'assets/images/abilities/passives/mirror/icon.png',
        'max_level': 5,
        'class': 'Mirror'
    },
    
    'overlevel':{  # +1 to max_level to all abilities excluding self, rare passive
        'name': 'overlevel',
        'display_name': 'Overlevel [•]',
        'icon': 'assets/images/abilities/passives/overlevel/icon.webp',
        'max_level': 1,
        'class': 'Overlevel'
    },
    
    'moreExp': {  # gives more exp when killing enemies
        'name': 'moreExp',
        'display_name': 'More Experience [•]',
        'icon': 'assets/images/abilities/passives/more experience/icon.png',
        'max_level': 3,
        'class': 'MoreExp'
    },
    
    'cheese': {  # allows you to revive once after death
        'name': 'cheese',
        'display_name': 'Cheese [•]',
        'icon': 'assets/images/abilities/passives/cheese/icon.png',
        'max_level': 1,
        'class': 'Cheese'
    }
}
