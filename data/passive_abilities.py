'''A module that stores passive abilities data'''
# name: Code name of the ability
# display_name: Display name of the ability
# icon: Path to the icon of the ability that appears in the upgrade menu
# sprite: Path to the sprites of the ability that appears in the game

# All passive abilities have '[•]' in their names
PASSIVE_ABILITIES: dict = {

    # +1 to projectiles per level for each ability a player has
    'duplicator': {
        'name': 'duplicator',
        'display_name': 'Duplicator [•]',
        'icon': 'assets/images/abilities/passives/duplicator/icon.png',
        'max_level': 3,
        'class': 'Duplicator'
    },

    # Reduces the cooldowns of all abilities
    'overclock': {
        'name': 'overclock',
        'display_name': 'Overclock [•]',
        'icon': 'assets/images/abilities/passives/overclock/icon.png',
        'max_level': 3,
        'class': 'Overclock'
    },

    # Clones random active ability
    'mirror': {
        'name': 'mirror',
        'display_name': 'Mirror [•]',
        'icon': 'assets/images/abilities/passives/mirror/icon.png',
        'max_level': 5,
        'class': 'Mirror'
    },

    # +1 to max_level to all abilities except self
    'overlvl':{
        'name': 'overlvl',
        'display_name': 'OverLvl [•]',
        'icon': 'assets/images/abilities/passives/overlevel/icon.webp',
        'max_level': 1,
        'class': 'OverLvl'
    },

    # Gives you more experience from killing enemies
    'more_exp': {
        'name': 'more_exp',
        'display_name': 'More Experience [•]',
        'icon': 'assets/images/abilities/passives/more experience/icon.png',
        'max_level': 3,
        'class': 'MoreExp'
    },

    # Allows you to respawn once after death
    'cheese': {
        'name': 'cheese',
        'display_name': 'Cheese [•]',
        'icon': 'assets/images/abilities/passives/cheese/icon.png',
        'max_level': 1,
        'class': 'Cheese'
    }
}
