# sprites: Path to the character's sprite folder with the walk animation
# scale_by: Number that determine the size increase of character sprites (Default: 1)
# characterPreview: Image that appears in the 'Character Select' menu 

CHARACTERS: dict = {    
    'Protagonist': {
        'sprites': 'assets/characters/protagonist/walk',
        'scale_by': 2.5,
        'characterPreview': 'assets/characters/protagonist/walk/1.png',
        'startAbility': 'shuriken',
        'hp': 100,
        'speed': 5
    }
}
