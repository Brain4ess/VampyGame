'''This module provides a function to retrieve the current configuration object.'''
import configparser as cfgp

cfg = cfgp.ConfigParser()
cfg.read('data/config.ini')

def get_config() -> cfgp.ConfigParser:
    """
    Get the current configuration object.
    
    Returns:
        object: The configuration object containing application settings.
    """
    return cfg
