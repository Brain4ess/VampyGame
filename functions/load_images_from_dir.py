'''Load images from a directory and apply optional transformations.'''
import os

import pygame as pg


def load_images_from_dir(path,
                         rotation: int = 0,
                         with_flip: bool = False,
                         flip_vertical: bool = False
):
    """
    Load images from a directory and apply optional transformations.
    
    This function loads all PNG images from the specified directory path and applies
    optional transformations including rotation, vertical flipping, and horizontal flipping.
    
    Args:
        path (str): The directory path containing PNG images numbered sequentially (1.png, 2.png, etc.)
        rotation (int, optional): Angle in degrees to rotate all images. Defaults to 0.
        with_flip (bool, optional): If True, returns both original and horizontally flipped versions. 
                                  Defaults to False.
        flip_vertical (bool, optional): If True, flips all images vertically. Defaults to False.
    
    Returns:
        list or tuple: 
            - If with_flip is False: Returns a list of pygame Surface objects
            - If with_flip is True: Returns a tuple containing (original_images, flipped_images)
                where both are lists of pygame Surface objects
    
    Note:
        - Requires pygame (pg) and os modules to be imported
        - Images must be named sequentially starting from 1.png
        - All transformations are applied in order: rotation, vertical flip, then horizontal flip
    """
    images = [pg.image.load(f'{path}/{i + 1}.png') for i in range(len(os.listdir(path)))]

    if rotation:
        images = [pg.transform.rotate(i, rotation) for i in images]

    if flip_vertical:
        images = [pg.transform.flip(i, flip_x=False, flip_y=True) for i in images]

    if with_flip:
        images_flipped = [pg.transform.flip(i, True, False) for i in images]
        return images, images_flipped

    return images
