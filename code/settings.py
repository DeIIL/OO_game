import pygame, sys
from pygame.math import Vector2 as vector

_WINDOW_WIDTH, _WINDOW_HEIGHT = 1280, 720
_TILE_SIZE = 64
_ANIMATION_SPEED = 6

# layers 
_Z_LAYERS = {
	'bg': 0,
	'clouds': 1,
	'bg tiles': 2,
	'path': 3,
	'bg details': 4,
	'main': 5,
	'water': 6,
	'fg': 7
}

# Getter functions for accessing private constants
def get_window_dimensions():
    return _WINDOW_WIDTH, _WINDOW_HEIGHT

def get_tile_size():
    return _TILE_SIZE

def get_animation_speed():
    return _ANIMATION_SPEED

def get_z_layers(layer_name):
    return _Z_LAYERS.get(layer_name, 0)