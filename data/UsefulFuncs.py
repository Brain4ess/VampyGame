import configparser as cfgp
import pygame as pg
import os

cfg = cfg = cfgp.ConfigParser()
cfg.read('data/config.ini')

def get_config():
    return cfg

def load_images_from_dir(path, rotation: int = 0, with_flip: bool = False, flip_vertical: bool = False):
    images = [pg.image.load(f'{path}/{i+1}.png') for i in range(len(os.listdir(path)))]
    if rotation != 0:
        images = [pg.transform.rotate(i, rotation) for i in images]
    if flip_vertical:
        images = [pg.transform.flip(i, flip_x=False,flip_y=True)for i in images]
    if with_flip:
        images_flipped = [pg.transform.flip(i, True, False) for i in images]
        return images, images_flipped
    return images
